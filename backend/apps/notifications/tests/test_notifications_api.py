"""
Тесты REST API уведомлений.
"""

from __future__ import annotations

from apps.notifications.constants import (
    NotificationCategory,
    NotificationLevel,
    NotificationSourceType,
    NotificationType,
)
from apps.notifications.services import build_deduplication_key, create_notification
from apps.notifications.tests.factories import create_test_user
from rest_framework import status
from rest_framework.test import APITestCase


class NotificationsApiTestCase(APITestCase):
    """
    Проверяет базовую работу API уведомлений.
    """

    def setUp(self) -> None:
        """
        Создаёт пользователей и тестовое уведомление.
        """

        self.user = create_test_user(
            email="student@example.com",
            phone="+79000000001",
            first_name="Иван",
            last_name="Петров",
        )

        self.other_user = create_test_user(
            email="other@example.com",
            phone="+79000000002",
            first_name="Анна",
            last_name="Сидорова",
        )

        self.base_url = "/api/v1/notifications/"
        self.me_url = "/api/v1/notifications/me/"
        self.unread_count_url = "/api/v1/notifications/me/unread-count/"
        self.read_all_url = "/api/v1/notifications/read-all/"
        self.bootstrap_url = "/api/v1/notifications/bootstrap/"

        self.notification, _created = create_notification(
            recipient=self.user,
            title="Тестовое уведомление",
            message="Это тестовое уведомление пользователя.",
            notification_type=NotificationType.SYSTEM,
            category=NotificationCategory.SYSTEM,
            level=NotificationLevel.INFO,
            source_type=NotificationSourceType.SYSTEM,
            source_id="api-test",
            deduplication_key=build_deduplication_key(
                user_id=self.user.id,
                notification_type=NotificationType.SYSTEM,
                source_type=NotificationSourceType.SYSTEM,
                source_id="api-test",
            ),
            action_label="Открыть",
            action_url="/student",
        )

    def authenticate(self) -> None:
        """
        Авторизует основного пользователя.
        """

        self.client.force_authenticate(user=self.user)

    def test_notifications_require_authentication(self) -> None:
        """
        Неавторизованный пользователь не может получить уведомления.
        """

        response = self.client.get(self.me_url)

        self.assertIn(
            response.status_code,
            [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ],
        )

    def test_user_can_get_notifications_feed(self) -> None:
        """
        Пользователь может получить свою ленту уведомлений.
        """

        self.authenticate()

        response = self.client.get(self.me_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("unread_count", response.data)
        self.assertIn("items", response.data)
        self.assertEqual(response.data["unread_count"], 1)
        self.assertEqual(len(response.data["items"]), 1)
        self.assertEqual(response.data["items"][0]["title"], "Тестовое уведомление")

    def test_user_can_get_unread_count(self) -> None:
        """
        Пользователь может получить количество непрочитанных уведомлений.
        """

        self.authenticate()

        response = self.client.get(self.unread_count_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["unread_count"], 1)

    def test_user_can_get_notification_detail(self) -> None:
        """
        Пользователь может получить детальную карточку своего уведомления.
        """

        self.authenticate()

        response = self.client.get(f"{self.base_url}{self.notification.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.notification.id)
        self.assertEqual(response.data["title"], "Тестовое уведомление")
        self.assertTrue(response.data["has_action"])

    def test_user_cannot_get_other_user_notification(self) -> None:
        """
        Пользователь не может получить чужое уведомление.
        """

        other_notification, _created = create_notification(
            recipient=self.other_user,
            title="Чужое уведомление",
            message="Это уведомление другого пользователя.",
            notification_type=NotificationType.SYSTEM,
            category=NotificationCategory.SYSTEM,
            level=NotificationLevel.INFO,
            source_type=NotificationSourceType.SYSTEM,
            source_id="other-api-test",
            deduplication_key=build_deduplication_key(
                user_id=self.other_user.id,
                notification_type=NotificationType.SYSTEM,
                source_type=NotificationSourceType.SYSTEM,
                source_id="other-api-test",
            ),
        )

        self.authenticate()

        response = self.client.get(f"{self.base_url}{other_notification.id}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_can_mark_notification_as_read(self) -> None:
        """
        Пользователь может отметить уведомление как прочитанное.
        """

        self.authenticate()

        response = self.client.post(f"{self.base_url}{self.notification.id}/read/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["notification"]["status"], "read")

        self.notification.refresh_from_db()
        self.assertEqual(self.notification.status, "read")
        self.assertIsNotNone(self.notification.read_at)
        self.assertIsNotNone(self.notification.expires_at)

    def test_user_can_mark_all_notifications_as_read(self) -> None:
        """
        Пользователь может отметить все уведомления как прочитанные.
        """

        self.authenticate()

        response = self.client.post(self.read_all_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["updated_count"], 1)
        self.assertEqual(response.data["unread_count"], 0)

    def test_user_can_complete_notification(self) -> None:
        """
        Пользователь может отметить уведомление как выполненное.
        """

        self.authenticate()

        response = self.client.post(f"{self.base_url}{self.notification.id}/complete/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["notification"]["status"], "completed")

        self.notification.refresh_from_db()
        self.assertEqual(self.notification.status, "completed")
        self.assertIsNotNone(self.notification.completed_at)

    def test_user_can_delete_notification(self) -> None:
        """
        Пользователь может удалить своё уведомление.
        """

        self.authenticate()

        response = self.client.delete(f"{self.base_url}{self.notification.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(
            self.user.notifications.filter(id=self.notification.id).exists()
        )

    def test_user_can_filter_unread_notifications(self) -> None:
        """
        API поддерживает фильтр unread_only.
        """

        self.notification.mark_as_read()

        create_notification(
            recipient=self.user,
            title="Новое уведомление",
            message="Это новое непрочитанное уведомление.",
            notification_type=NotificationType.SYSTEM,
            category=NotificationCategory.SYSTEM,
            level=NotificationLevel.INFO,
            source_type=NotificationSourceType.SYSTEM,
            source_id="unread-filter-test",
            deduplication_key=build_deduplication_key(
                user_id=self.user.id,
                notification_type=NotificationType.SYSTEM,
                source_type=NotificationSourceType.SYSTEM,
                source_id="unread-filter-test",
            ),
        )

        self.authenticate()

        response = self.client.get(
            self.me_url,
            data={
                "unread_only": True,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["items"]), 1)
        self.assertEqual(response.data["items"][0]["title"], "Новое уведомление")
