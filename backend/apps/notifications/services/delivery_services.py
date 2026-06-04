"""
Сервисы доставки уведомлений.

Сейчас здесь зафиксирован контракт для внутренней WebSocket-доставки.
Email/VK/MAX будут подключены отдельными адаптерами.
"""

from __future__ import annotations

from apps.notifications.constants import (
    NotificationDeliveryChannel,
    NotificationDeliveryStatus,
)


def mark_delivery_sent(*, notification, channel: str, save: bool = True):
    """
    Отмечает доставку уведомления по каналу как успешную.
    """

    update_delivery_status(
        notification=notification,
        channel=channel,
        status=NotificationDeliveryStatus.SENT,
        save=save,
    )

    return notification


def mark_delivery_failed(*, notification, channel: str, save: bool = True):
    """
    Отмечает доставку уведомления по каналу как ошибочную.
    """

    update_delivery_status(
        notification=notification,
        channel=channel,
        status=NotificationDeliveryStatus.FAILED,
        save=save,
    )

    return notification


def mark_delivery_skipped(*, notification, channel: str, save: bool = True):
    """
    Отмечает доставку уведомления по каналу как пропущенную.
    """

    update_delivery_status(
        notification=notification,
        channel=channel,
        status=NotificationDeliveryStatus.SKIPPED,
        save=save,
    )

    return notification


def update_delivery_status(
    *,
    notification,
    channel: str,
    status: str,
    save: bool = True,
) -> None:
    """
    Обновляет статус доставки уведомления по конкретному каналу.
    """

    delivery_statuses = notification.delivery_statuses or {}
    delivery_statuses[channel] = status
    notification.delivery_statuses = delivery_statuses

    if save:
        notification.save(
            update_fields=[
                "delivery_statuses",
                "updated_at",
            ],
        )


def should_deliver_in_app(*, notification) -> bool:
    """
    Проверяет, нужно ли доставлять уведомление внутри платформы.
    """

    return NotificationDeliveryChannel.IN_APP in notification.delivery_channels


def deliver_notification_in_app(*, notification) -> None:
    """
    Доставляет уведомление внутри платформы.

    WebSocket будет подключён отдельным этапом через Django Channels.
    Сейчас функция фиксирует точку входа для будущей доставки.
    """

    if not should_deliver_in_app(notification=notification):
        mark_delivery_skipped(
            notification=notification,
            channel=NotificationDeliveryChannel.IN_APP,
        )
        return

    mark_delivery_sent(
        notification=notification,
        channel=NotificationDeliveryChannel.IN_APP,
    )
