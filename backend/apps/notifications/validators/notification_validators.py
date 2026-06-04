"""
Валидаторы модели уведомления.
"""

from __future__ import annotations

from apps.notifications.constants import NotificationDeliveryChannel
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def clean_notification_instance(notification) -> None:
    """
    Валидирует объект уведомления.
    """

    clean_notification_text_fields(notification)
    clean_notification_action_fields(notification)
    clean_notification_delivery_channels(notification)
    clean_notification_dates(notification)


def clean_notification_text_fields(notification) -> None:
    """
    Очищает и валидирует строковые поля уведомления.
    """

    notification.title = notification.title.strip()
    notification.message = notification.message.strip()
    notification.source_id = notification.source_id.strip()
    notification.deduplication_key = notification.deduplication_key.strip()
    notification.action_label = notification.action_label.strip()
    notification.action_url = notification.action_url.strip()

    if not notification.title:
        raise ValidationError(
            {
                "title": _("Заголовок уведомления не может быть пустым."),
            },
        )

    if not notification.message:
        raise ValidationError(
            {
                "message": _("Сообщение уведомления не может быть пустым."),
            },
        )

    if not notification.deduplication_key:
        raise ValidationError(
            {
                "deduplication_key": _(
                    "Ключ дедупликации уведомления не может быть пустым."
                ),
            },
        )


def clean_notification_action_fields(notification) -> None:
    """
    Проверяет корректность действия уведомления.
    """

    if notification.action_label and not notification.action_url:
        raise ValidationError(
            {
                "action_url": _(
                    "Если указан текст действия, нужно указать ссылку действия."
                ),
            },
        )

    if notification.action_url and not notification.action_label:
        raise ValidationError(
            {
                "action_label": _(
                    "Если указана ссылка действия, нужно указать текст действия."
                ),
            },
        )


def clean_notification_delivery_channels(notification) -> None:
    """
    Проверяет каналы доставки уведомления.
    """

    if not isinstance(notification.delivery_channels, list):
        raise ValidationError(
            {
                "delivery_channels": _("Каналы доставки должны быть списком."),
            },
        )

    allowed_channels = {channel.value for channel in NotificationDeliveryChannel}

    invalid_channels = [
        channel
        for channel in notification.delivery_channels
        if channel not in allowed_channels
    ]

    if invalid_channels:
        raise ValidationError(
            {
                "delivery_channels": _("Найдены недопустимые каналы доставки."),
            },
        )


def clean_notification_dates(notification) -> None:
    """
    Проверяет согласованность дат уведомления.
    """

    if (
        notification.completed_at
        and notification.read_at
        and notification.completed_at < notification.read_at
    ):
        raise ValidationError(
            {
                "completed_at": _(
                    "Дата выполнения не может быть раньше даты прочтения."
                ),
            },
        )

    if (
        notification.expires_at
        and notification.created_at
        and notification.expires_at < notification.created_at
    ):
        raise ValidationError(
            {
                "expires_at": _("Дата удаления не может быть раньше даты создания."),
            },
        )
