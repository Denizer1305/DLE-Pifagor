"""
Сервисы уведомлений по событиям календаря.
"""

from __future__ import annotations

from apps.notifications.constants import (
    NotificationCategory,
    NotificationLevel,
    NotificationSourceType,
    NotificationType,
)
from apps.notifications.selectors import get_calendar_events_for_user
from apps.notifications.services.notification_services import (
    build_deduplication_key,
    create_notification,
)
from django.utils import timezone


def create_calendar_event_notifications_for_user(
    *,
    user,
    target_date=None,
) -> list:
    """
    Создаёт уведомления о событиях календаря на выбранную дату.
    """

    target_date = target_date or timezone.localdate()
    events = get_calendar_events_for_user(
        user=user,
        target_date=target_date,
    )

    created_notifications = []

    for event in events:
        notification, created = create_calendar_event_notification(
            user=user,
            event=event,
            target_date=target_date,
        )

        if created:
            created_notifications.append(notification)

    return created_notifications


def create_calendar_event_notification(*, user, event, target_date):
    """
    Создаёт уведомление о событии календаря.
    """

    event_id = get_source_attr(event, "id", "")
    event_title = get_source_attr(event, "title", "Событие календаря")
    event_at = get_source_attr(event, "starts_at", None)

    deduplication_key = build_deduplication_key(
        user_id=user.id,
        notification_type=NotificationType.CALENDAR_EVENT_TODAY,
        source_type=NotificationSourceType.CALENDAR_EVENT,
        source_id=event_id,
        target_date=target_date,
    )

    return create_notification(
        recipient=user,
        title="Событие календаря сегодня",
        message=f"Сегодня запланировано событие: {event_title}.",
        notification_type=NotificationType.CALENDAR_EVENT_TODAY,
        category=NotificationCategory.CALENDAR,
        level=NotificationLevel.INFO,
        source_type=NotificationSourceType.CALENDAR_EVENT,
        source_id=str(event_id),
        deduplication_key=deduplication_key,
        action_label="Открыть календарь",
        action_url=build_calendar_action_url(user=user),
        event_at=event_at,
        payload={
            "event_id": event_id,
            "event_title": event_title,
            "target_date": target_date.isoformat(),
        },
    )


def build_calendar_action_url(*, user) -> str:
    """
    Возвращает ссылку на календарь по роли пользователя.
    """

    role_code = get_user_role_code(user)

    if role_code == "teacher":
        return "/teacher/calendar"

    if role_code == "guardian":
        return "/parent/calendar"

    if role_code == "admin":
        return "/admin/calendar"

    return "/student/calendar"


def get_user_role_code(user) -> str:
    """
    Возвращает активную роль пользователя.
    """

    settings_obj = getattr(user, "settings", None)

    if settings_obj and settings_obj.active_role:
        return settings_obj.active_role

    if user.is_superuser:
        return "admin"

    return "learner"


def get_source_attr(source, attr: str, default=""):
    """
    Безопасно получает атрибут из объекта или словаря.
    """

    if isinstance(source, dict):
        return source.get(attr, default)

    return getattr(source, attr, default)
