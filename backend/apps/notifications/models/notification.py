"""
Модель внутреннего уведомления платформы.
"""

from __future__ import annotations

from apps.notifications.constants import (
    NOTIFICATION_ACTION_LABEL_MAX_LENGTH,
    NOTIFICATION_ACTION_URL_MAX_LENGTH,
    NOTIFICATION_DEDUPLICATION_KEY_MAX_LENGTH,
    NOTIFICATION_MESSAGE_MAX_LENGTH,
    NOTIFICATION_SOURCE_ID_MAX_LENGTH,
    NOTIFICATION_TITLE_MAX_LENGTH,
    NotificationCategory,
    NotificationLevel,
    NotificationRole,
    NotificationSourceType,
    NotificationStatus,
    NotificationType,
)
from apps.notifications.managers import NotificationManager
from apps.notifications.models.notification_mixins import NotificationLifecycleMixin
from apps.notifications.validators import clean_notification_instance
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Notification(NotificationLifecycleMixin, models.Model):
    """
    Внутреннее уведомление пользователя.

    Модель хранит событие, которое должно быть показано пользователю
    внутри платформы: ежедневная сводка, дедлайн, событие календаря,
    напоминание заметки, день рождения, системное сообщение или событие
    безопасности.
    """

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name=_("Получатель"),
    )

    title = models.CharField(
        _("Заголовок"),
        max_length=NOTIFICATION_TITLE_MAX_LENGTH,
    )
    message = models.TextField(
        _("Сообщение"),
        max_length=NOTIFICATION_MESSAGE_MAX_LENGTH,
    )

    notification_type = models.CharField(
        _("Тип уведомления"),
        max_length=64,
        choices=NotificationType.choices,
        db_index=True,
    )
    category = models.CharField(
        _("Категория"),
        max_length=64,
        choices=NotificationCategory.choices,
        db_index=True,
    )
    level = models.CharField(
        _("Уровень важности"),
        max_length=24,
        choices=NotificationLevel.choices,
        default=NotificationLevel.INFO,
        db_index=True,
    )
    status = models.CharField(
        _("Статус"),
        max_length=24,
        choices=NotificationStatus.choices,
        default=NotificationStatus.UNREAD,
        db_index=True,
    )
    recipient_role = models.CharField(
        _("Роль получателя"),
        max_length=32,
        choices=NotificationRole.choices,
        blank=True,
        default="",
        db_index=True,
    )

    source_type = models.CharField(
        _("Тип источника"),
        max_length=64,
        choices=NotificationSourceType.choices,
        default=NotificationSourceType.SYSTEM,
        db_index=True,
    )
    source_id = models.CharField(
        _("ID источника"),
        max_length=NOTIFICATION_SOURCE_ID_MAX_LENGTH,
        blank=True,
        default="",
        db_index=True,
    )

    deduplication_key = models.CharField(
        _("Ключ дедупликации"),
        max_length=NOTIFICATION_DEDUPLICATION_KEY_MAX_LENGTH,
        unique=True,
        db_index=True,
        help_text=_(
            "Ключ, который не позволяет создать одно и то же уведомление "
            "несколько раз за один период."
        ),
    )

    action_label = models.CharField(
        _("Текст действия"),
        max_length=NOTIFICATION_ACTION_LABEL_MAX_LENGTH,
        blank=True,
        default="",
    )
    action_url = models.CharField(
        _("Ссылка действия"),
        max_length=NOTIFICATION_ACTION_URL_MAX_LENGTH,
        blank=True,
        default="",
    )

    delivery_channels = models.JSONField(
        _("Каналы доставки"),
        default=list,
        blank=True,
        help_text=_("Список каналов доставки: in_app, email, vk, max."),
    )
    delivery_statuses = models.JSONField(
        _("Статусы доставки"),
        default=dict,
        blank=True,
        help_text=_("Состояние доставки уведомления по каналам."),
    )
    payload = models.JSONField(
        _("Дополнительные данные"),
        default=dict,
        blank=True,
        help_text=_("Технические данные для frontend, WebSocket и доставок."),
    )

    event_at = models.DateTimeField(
        _("Дата события"),
        null=True,
        blank=True,
        db_index=True,
        help_text=_(
            "Дата события, к которому относится уведомление: дедлайн, "
            "напоминание, контрольная или событие календаря."
        ),
    )
    read_at = models.DateTimeField(
        _("Дата прочтения"),
        null=True,
        blank=True,
    )
    completed_at = models.DateTimeField(
        _("Дата выполнения"),
        null=True,
        blank=True,
    )
    expires_at = models.DateTimeField(
        _("Дата удаления"),
        null=True,
        blank=True,
        db_index=True,
        help_text=_("После этой даты уведомление может быть удалено задачей очистки."),
    )

    created_at = models.DateTimeField(
        _("Дата создания"),
        auto_now_add=True,
        db_index=True,
    )
    updated_at = models.DateTimeField(
        _("Дата обновления"),
        auto_now=True,
    )

    objects = NotificationManager()

    class Meta:
        """
        Мета-настройки модели уведомления.
        """

        verbose_name = _("Уведомление")
        verbose_name_plural = _("Уведомления")
        ordering = [
            "status",
            "-created_at",
            "-id",
        ]
        indexes = [
            models.Index(
                fields=[
                    "recipient",
                    "status",
                    "-created_at",
                ],
                name="notif_user_status_created_idx",
            ),
            models.Index(
                fields=[
                    "recipient",
                    "category",
                    "-created_at",
                ],
                name="notif_user_category_idx",
            ),
            models.Index(
                fields=[
                    "recipient",
                    "notification_type",
                    "-created_at",
                ],
                name="notif_user_type_idx",
            ),
            models.Index(
                fields=[
                    "source_type",
                    "source_id",
                ],
                name="notif_source_idx",
            ),
            models.Index(
                fields=[
                    "expires_at",
                ],
                name="notif_expires_idx",
            ),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление уведомления.
        """

        return f"{self.title} → {self.recipient}"

    def clean(self) -> None:
        """
        Валидирует внутреннюю согласованность уведомления.
        """

        super().clean()
        clean_notification_instance(self)
