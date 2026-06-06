"""
Базовые сервисы уведомлений.

Файл содержит основные операции с уведомлениями:
создание без дублей, отметка как прочитанное, выполнение, архивирование,
удаление и подготовка ключей дедупликации.
"""

from __future__ import annotations

from django.db import IntegrityError, transaction
from django.utils import timezone

from apps.notifications.constants import (
    NotificationCategory,
    NotificationDeliveryChannel,
    NotificationDeliveryStatus,
    NotificationLevel,
    NotificationSourceType,
    NotificationStatus,
    NotificationType,
)
from apps.notifications.models import Notification
from apps.notifications.selectors import (
    get_notification_by_deduplication_key,
    get_user_active_notification_by_id,
)
from apps.notifications.services.notification_preference_services import (
    resolve_delivery_channels_for_recipient,
    should_create_notification_for_recipient,
)


@transaction.atomic
def create_notification(
    *,
    recipient,
    title: str,
    message: str,
    notification_type: str,
    category: str,
    level: str = NotificationLevel.INFO,
    recipient_role: str = "",
    source_type: str = NotificationSourceType.SYSTEM,
    source_id: str = "",
    deduplication_key: str,
    action_label: str = "",
    action_url: str = "",
    delivery_channels: list[str] | None = None,
    payload: dict | None = None,
    event_at=None,
) -> tuple[Notification | None, bool]:
    """
    Создаёт уведомление без дублей.

    Возвращает пару:
    - объект уведомления;
    - флаг created, который показывает, было ли уведомление создано.
    """

    if not should_create_notification_for_recipient(
        recipient=recipient,
        category=category,
        level=level,
    ):
        return None, False

    existing_notification = get_notification_by_deduplication_key(
        deduplication_key,
    )

    if existing_notification:
        return existing_notification, False

    normalized_channels = resolve_delivery_channels_for_recipient(
        recipient=recipient,
        category=category,
        level=level,
        channels=delivery_channels,
    )

    if not normalized_channels:
        return None, False

    delivery_statuses = build_initial_delivery_statuses(normalized_channels)

    notification = Notification(
        recipient=recipient,
        title=title,
        message=message,
        notification_type=notification_type,
        category=category,
        level=level,
        status=NotificationStatus.UNREAD,
        recipient_role=recipient_role,
        source_type=source_type,
        source_id=str(source_id or ""),
        deduplication_key=deduplication_key,
        action_label=action_label,
        action_url=action_url,
        delivery_channels=normalized_channels,
        delivery_statuses=delivery_statuses,
        payload=payload or {},
        event_at=event_at,
    )

    notification.full_clean()

    try:
        notification.save()
    except IntegrityError:
        existing_notification = get_notification_by_deduplication_key(
            deduplication_key,
        )

        if existing_notification:
            return existing_notification, False

        raise

    return notification, True


@transaction.atomic
def mark_notification_as_read(*, user, notification_id: int) -> Notification:
    """
    Отмечает уведомление пользователя как прочитанное.
    """

    notification = get_user_active_notification_by_id(
        user=user,
        notification_id=notification_id,
    )

    notification.mark_as_read()

    return notification


@transaction.atomic
def mark_all_notifications_as_read(*, user) -> int:
    """
    Отмечает все непрочитанные уведомления пользователя как прочитанные.

    Возвращает количество изменённых уведомлений.
    """

    now = timezone.now()
    expires_at = get_default_expiration_at()

    queryset = Notification.objects.unread_for_user(user)

    return queryset.update(
        status=NotificationStatus.READ,
        read_at=now,
        expires_at=expires_at,
        updated_at=now,
    )


@transaction.atomic
def complete_notification(*, user, notification_id: int) -> Notification:
    """
    Отмечает уведомление пользователя как выполненное.
    """

    notification = get_user_active_notification_by_id(
        user=user,
        notification_id=notification_id,
    )

    notification.mark_as_completed()

    return notification


@transaction.atomic
def archive_notification(*, user, notification_id: int) -> Notification:
    """
    Архивирует уведомление пользователя.
    """

    notification = get_user_active_notification_by_id(
        user=user,
        notification_id=notification_id,
    )

    notification.archive()

    return notification


@transaction.atomic
def delete_notification(*, user, notification_id: int) -> None:
    """
    Удаляет уведомление пользователя.
    """

    notification = get_user_active_notification_by_id(
        user=user,
        notification_id=notification_id,
    )

    if delete_dashboard_source_for_notification(user=user, notification=notification):
        return

    notification.delete()


def delete_dashboard_source_for_notification(*, user, notification) -> bool:
    source_kind = {
        NotificationSourceType.CALENDAR_EVENT: "calendar",
        NotificationSourceType.NOTE: "note",
    }.get(notification.source_type)

    if not source_kind or not notification.source_id.isdigit():
        return False

    from apps.dashboard.models import DashboardItem
    from apps.dashboard.services.dashboard_item_services import delete_dashboard_item

    item = DashboardItem.objects.filter(
        user=user,
        id=int(notification.source_id),
        kind=source_kind,
    ).first()

    if not item:
        return False

    delete_dashboard_item(item=item)

    return True


def build_deduplication_key(
    *,
    user_id: int | str,
    notification_type: str,
    source_type: str = NotificationSourceType.SYSTEM,
    source_id: int | str = "",
    target_date=None,
) -> str:
    """
    Формирует ключ дедупликации уведомления.

    Ключ должен гарантировать, что одно и то же уведомление не будет создано
    больше одного раза за нужный период.
    """

    date_part = ""

    if target_date:
        date_part = f":{target_date.isoformat()}"

    source_part = str(source_id or "none")

    return (
        f"{notification_type}:"
        f"user:{user_id}:"
        f"source:{source_type}:"
        f"{source_part}"
        f"{date_part}"
    )


def normalize_delivery_channels(
    channels: list[str] | None,
) -> list[str]:
    """
    Нормализует список каналов доставки.

    Внутренний канал in_app добавляется всегда, если список не передан.
    """

    if not channels:
        return [
            NotificationDeliveryChannel.IN_APP,
        ]

    normalized_channels = []

    for channel in channels:
        if channel not in normalized_channels:
            normalized_channels.append(channel)

    if NotificationDeliveryChannel.IN_APP not in normalized_channels:
        normalized_channels.append(NotificationDeliveryChannel.IN_APP)

    return normalized_channels


def build_initial_delivery_statuses(
    channels: list[str],
) -> dict:
    """
    Создаёт начальные статусы доставки по каналам.
    """

    return {channel: NotificationDeliveryStatus.PENDING for channel in channels}


def get_default_expiration_at():
    """
    Возвращает дату удаления уведомления после прочтения или выполнения.
    """

    from datetime import timedelta

    from apps.notifications.constants import (
        NOTIFICATION_RETENTION_DAYS_AFTER_COMPLETION,
    )

    return timezone.now() + timedelta(
        days=NOTIFICATION_RETENTION_DAYS_AFTER_COMPLETION,
    )


def create_system_notification(
    *,
    recipient,
    title: str,
    message: str,
    level: str = NotificationLevel.INFO,
    deduplication_key: str,
    action_label: str = "",
    action_url: str = "",
    payload: dict | None = None,
) -> tuple[Notification | None, bool]:
    """
    Создаёт системное уведомление.
    """

    return create_notification(
        recipient=recipient,
        title=title,
        message=message,
        notification_type=NotificationType.SYSTEM,
        category=NotificationCategory.SYSTEM,
        level=level,
        source_type=NotificationSourceType.SYSTEM,
        deduplication_key=deduplication_key,
        action_label=action_label,
        action_url=action_url,
        payload=payload or {},
    )


def create_security_notification(
    *,
    recipient,
    title: str,
    message: str,
    level: str = NotificationLevel.DANGER,
    deduplication_key: str,
    action_label: str = "",
    action_url: str = "",
    payload: dict | None = None,
) -> tuple[Notification | None, bool]:
    """
    Создаёт уведомление безопасности.
    """

    return create_notification(
        recipient=recipient,
        title=title,
        message=message,
        notification_type=NotificationType.SECURITY,
        category=NotificationCategory.SECURITY,
        level=level,
        source_type=NotificationSourceType.SECURITY_EVENT,
        deduplication_key=deduplication_key,
        action_label=action_label,
        action_url=action_url,
        payload=payload or {},
    )
