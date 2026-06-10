"""
Тесты очистки уведомлений.
"""

from __future__ import annotations

from datetime import timedelta

from apps.notifications.constants import (
    NotificationCategory,
    NotificationLevel,
    NotificationSourceType,
    NotificationType,
)
from apps.notifications.models import Notification
from apps.notifications.services import (
    build_deduplication_key,
    cleanup_expired_notifications,
    create_notification,
)
from apps.notifications.tests.factories import create_test_user
from django.utils import timezone
from rest_framework.test import APITestCase


class NotificationCleanupTestCase(APITestCase):
    """
    Проверяет очистку уведомлений.
    """

    def setUp(self) -> None:
        """
        Создаёт пользователя.
        """

        self.user = create_test_user(
            email="cleanup@example.com",
            phone="+79990000105",
            password="StrongPassword123!",
            first_name="Павел",
            last_name="Смирнов",
        )

    def create_test_notification(self, *, source_id: str):
        """
        Создаёт тестовое уведомление.
        """

        notification, _created = create_notification(
            recipient=self.user,
            title="Уведомление для очистки",
            message="Это уведомление используется в тестах очистки.",
            notification_type=NotificationType.SYSTEM,
            category=NotificationCategory.SYSTEM,
            level=NotificationLevel.INFO,
            source_type=NotificationSourceType.SYSTEM,
            source_id=source_id,
            deduplication_key=build_deduplication_key(
                user_id=self.user.id,
                notification_type=NotificationType.SYSTEM,
                source_type=NotificationSourceType.SYSTEM,
                source_id=source_id,
            ),
        )

        return notification

    def test_cleanup_deletes_expired_notifications(self) -> None:
        """
        Очистка удаляет уведомления с истёкшим expires_at.
        """

        notification = self.create_test_notification(source_id="expired")
        notification.expires_at = timezone.now() - timedelta(days=1)
        notification.save(update_fields=["expires_at", "updated_at"])

        deleted_count = cleanup_expired_notifications()

        self.assertEqual(deleted_count, 1)
        self.assertFalse(Notification.objects.filter(id=notification.id).exists())

    def test_cleanup_keeps_active_notifications(self) -> None:
        """
        Очистка не удаляет активные уведомления.
        """

        notification = self.create_test_notification(source_id="active")
        notification.expires_at = timezone.now() + timedelta(days=7)
        notification.save(update_fields=["expires_at", "updated_at"])

        deleted_count = cleanup_expired_notifications()

        self.assertEqual(deleted_count, 0)
        self.assertTrue(Notification.objects.filter(id=notification.id).exists())

    def test_mark_as_read_sets_expiration(self) -> None:
        """
        После прочтения уведомление получает дату удаления.
        """

        notification = self.create_test_notification(source_id="read-expiration")

        notification.mark_as_read()
        notification.refresh_from_db()

        self.assertEqual(notification.status, "read")
        self.assertIsNotNone(notification.read_at)
        self.assertIsNotNone(notification.expires_at)

    def test_mark_as_completed_sets_expiration(self) -> None:
        """
        После выполнения уведомление получает дату удаления.
        """

        notification = self.create_test_notification(source_id="completed-expiration")

        notification.mark_as_completed()
        notification.refresh_from_db()

        self.assertEqual(notification.status, "completed")
        self.assertIsNotNone(notification.completed_at)
        self.assertIsNotNone(notification.expires_at)
