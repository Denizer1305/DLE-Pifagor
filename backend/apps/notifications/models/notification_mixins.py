"""
Миксины модели уведомления.

Здесь находится поведение уведомления: статусы, прочтение, выполнение,
архивация, срок хранения и работа с внутренним каналом доставки.
"""

from __future__ import annotations

from datetime import timedelta

from apps.notifications.constants import (
    NOTIFICATION_RETENTION_DAYS_AFTER_COMPLETION,
    NotificationDeliveryChannel,
    NotificationStatus,
)
from django.utils import timezone


class NotificationLifecycleMixin:
    """
    Миксин жизненного цикла уведомления.
    """

    @property
    def is_unread(self) -> bool:
        """
        Проверяет, является ли уведомление непрочитанным.
        """

        return self.status == NotificationStatus.UNREAD

    @property
    def is_read(self) -> bool:
        """
        Проверяет, является ли уведомление прочитанным.
        """

        return self.status == NotificationStatus.READ

    @property
    def is_completed(self) -> bool:
        """
        Проверяет, является ли уведомление выполненным.
        """

        return self.status == NotificationStatus.COMPLETED

    @property
    def is_archived(self) -> bool:
        """
        Проверяет, находится ли уведомление в архиве.
        """

        return self.status == NotificationStatus.ARCHIVED

    @property
    def is_expired(self) -> bool:
        """
        Проверяет, истёк ли срок хранения уведомления.
        """

        return bool(self.expires_at and self.expires_at <= timezone.now())

    @property
    def has_action(self) -> bool:
        """
        Проверяет, есть ли у уведомления действие для перехода.
        """

        return bool(self.action_label and self.action_url)

    def mark_as_read(self, *, save: bool = True) -> None:
        """
        Отмечает уведомление как прочитанное.
        """

        if self.status != NotificationStatus.UNREAD:
            return

        self.status = NotificationStatus.READ
        self.read_at = timezone.now()
        self.set_expiration_after_completion(save=False)

        if save:
            self.save(
                update_fields=[
                    "status",
                    "read_at",
                    "expires_at",
                    "updated_at",
                ],
            )

    def mark_as_completed(self, *, save: bool = True) -> None:
        """
        Отмечает уведомление как выполненное.
        """

        self.status = NotificationStatus.COMPLETED
        self.completed_at = timezone.now()
        self.set_expiration_after_completion(save=False)

        if save:
            self.save(
                update_fields=[
                    "status",
                    "completed_at",
                    "expires_at",
                    "updated_at",
                ],
            )

    def archive(self, *, save: bool = True) -> None:
        """
        Переводит уведомление в архив.
        """

        self.status = NotificationStatus.ARCHIVED
        self.set_expiration_after_completion(save=False)

        if save:
            self.save(
                update_fields=[
                    "status",
                    "expires_at",
                    "updated_at",
                ],
            )

    def set_expiration_after_completion(self, *, save: bool = True) -> None:
        """
        Назначает дату удаления уведомления после прочтения или выполнения.
        """

        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(
                days=NOTIFICATION_RETENTION_DAYS_AFTER_COMPLETION,
            )

        if save:
            self.save(
                update_fields=[
                    "expires_at",
                    "updated_at",
                ],
            )

    def ensure_in_app_channel(self) -> None:
        """
        Гарантирует наличие внутреннего канала доставки.
        """

        if not isinstance(self.delivery_channels, list):
            self.delivery_channels = []

        if NotificationDeliveryChannel.IN_APP not in self.delivery_channels:
            self.delivery_channels = [
                *self.delivery_channels,
                NotificationDeliveryChannel.IN_APP,
            ]
