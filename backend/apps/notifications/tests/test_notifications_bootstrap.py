"""
Тесты bootstrap-синхронизации уведомлений.
"""

from __future__ import annotations

from datetime import date
from unittest.mock import patch

from apps.notifications.constants import NotificationType
from apps.notifications.services import bootstrap_notifications_for_user
from apps.notifications.tests.factories import create_test_user
from rest_framework import status
from rest_framework.test import APITestCase


class NotificationsBootstrapTestCase(APITestCase):
    """
    Проверяет bootstrap уведомлений пользователя.
    """

    def setUp(self) -> None:
        """
        Создаёт пользователя.
        """

        self.user = create_test_user(
            email="birthday@example.com",
            phone="+79000000003",
            first_name="Денис",
            last_name="Быков",
        )
        self.bootstrap_url = "/api/v1/notifications/bootstrap/"

    def test_bootstrap_creates_birthday_notification_once(self) -> None:
        """
        Bootstrap создаёт поздравление с днём рождения только один раз.
        """

        target_date = date(2026, 5, 24)
        self.user.birth_date = date(2005, 5, 24)

        first_result = bootstrap_notifications_for_user(
            user=self.user,
            target_date=target_date,
        )
        second_result = bootstrap_notifications_for_user(
            user=self.user,
            target_date=target_date,
        )

        self.assertEqual(first_result["created_count"], 1)
        self.assertEqual(second_result["created_count"], 0)

        birthday_count = self.user.notifications.filter(
            notification_type=NotificationType.BIRTHDAY,
        ).count()

        self.assertEqual(birthday_count, 1)

    def test_bootstrap_does_not_create_daily_summary_without_sources(self) -> None:
        """
        Bootstrap не создаёт ежедневную сводку, если нет задач и событий.
        """

        target_date = date(2026, 5, 24)

        result = bootstrap_notifications_for_user(
            user=self.user,
            target_date=target_date,
        )

        self.assertEqual(result["created_count"], 0)

    @patch(
        "apps.notifications.services.daily_summary_services."
        "get_today_schedule_items_for_user"
    )
    def test_bootstrap_creates_daily_summary_with_schedule_items(
        self,
        mocked_schedule,
    ) -> None:
        """
        Bootstrap создаёт ежедневную сводку, если есть события на день.
        """

        target_date = date(2026, 5, 24)
        mocked_schedule.return_value = [
            {
                "id": 1,
                "title": "Математика",
            }
        ]

        result = bootstrap_notifications_for_user(
            user=self.user,
            target_date=target_date,
        )

        self.assertEqual(result["created_count"], 1)

        self.assertTrue(
            self.user.notifications.filter(
                notification_type=NotificationType.DAILY_SUMMARY,
            ).exists()
        )

    def test_bootstrap_api_returns_payload(self) -> None:
        """
        API bootstrap возвращает статистику синхронизации.
        """

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.bootstrap_url,
            data={
                "reason": "dashboard_login",
                "target_date": "2026-05-24",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("target_date", response.data)
        self.assertIn("created_count", response.data)
        self.assertIn("created_ids", response.data)
        self.assertIn("unread_count", response.data)
