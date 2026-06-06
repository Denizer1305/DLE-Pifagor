"""
Тесты сервисов генерации уведомлений.
"""

from __future__ import annotations

from datetime import date, datetime
from unittest.mock import patch

from django.utils import timezone
from rest_framework.test import APITestCase

from apps.notifications.constants import (
    NotificationCategory,
    NotificationLevel,
    NotificationSourceType,
    NotificationType,
)
from apps.notifications.services import (
    build_deduplication_key,
    create_assignment_deadline_notifications_for_user,
    create_birthday_notification,
    create_calendar_event_notifications_for_user,
    create_daily_summary_notification,
    create_note_reminder_notifications_for_user,
    create_notification,
)
from apps.notifications.tests.factories import create_test_user
from apps.users.models import UserSettings


class NotificationGenerationTestCase(APITestCase):
    """
    Проверяет генерацию уведомлений сервисным слоем.
    """

    def setUp(self) -> None:
        """
        Создаёт пользователя.
        """

        self.user = create_test_user(
            email="generation@example.com",
            phone="+79990000104",
            password="StrongPassword123!",
            first_name="Мария",
            last_name="Иванова",
        )

    def set_notification_settings(self, notification_settings: dict) -> None:
        settings, _ = UserSettings.objects.get_or_create(user=self.user)
        settings.notification_settings = notification_settings
        settings.save(update_fields=["notification_settings", "updated_at"])

    def test_create_notification_is_idempotent_by_deduplication_key(self) -> None:
        """
        create_notification не создаёт дубли при одинаковом deduplication_key.
        """

        key = build_deduplication_key(
            user_id=self.user.id,
            notification_type=NotificationType.SYSTEM,
            source_type=NotificationSourceType.SYSTEM,
            source_id="same-key",
        )

        first_notification, first_created = create_notification(
            recipient=self.user,
            title="Первое уведомление",
            message="Первое сообщение.",
            notification_type=NotificationType.SYSTEM,
            category=NotificationCategory.SYSTEM,
            level=NotificationLevel.INFO,
            source_type=NotificationSourceType.SYSTEM,
            source_id="same-key",
            deduplication_key=key,
        )
        second_notification, second_created = create_notification(
            recipient=self.user,
            title="Второе уведомление",
            message="Второе сообщение.",
            notification_type=NotificationType.SYSTEM,
            category=NotificationCategory.SYSTEM,
            level=NotificationLevel.INFO,
            source_type=NotificationSourceType.SYSTEM,
            source_id="same-key",
            deduplication_key=key,
        )

        self.assertTrue(first_created)
        self.assertFalse(second_created)
        self.assertEqual(first_notification.id, second_notification.id)
        self.assertEqual(self.user.notifications.count(), 1)

    def test_disabled_in_app_channel_suppresses_regular_notification(self) -> None:
        self.set_notification_settings(
            {
                "channels": {
                    "in_app": False,
                    "email": True,
                    "vk": False,
                    "max": False,
                }
            }
        )

        key = build_deduplication_key(
            user_id=self.user.id,
            notification_type=NotificationType.SYSTEM,
            source_type=NotificationSourceType.SYSTEM,
            source_id="hidden-by-settings",
        )

        notification, created = create_notification(
            recipient=self.user,
            title="Уведомление",
            message="Обычное сообщение.",
            notification_type=NotificationType.SYSTEM,
            category=NotificationCategory.EDUCATION,
            level=NotificationLevel.INFO,
            source_type=NotificationSourceType.SYSTEM,
            source_id="hidden-by-settings",
            deduplication_key=key,
        )

        self.assertIsNone(notification)
        self.assertFalse(created)
        self.assertEqual(self.user.notifications.count(), 0)

    def test_critical_notification_ignores_disabled_in_app_channel(self) -> None:
        self.set_notification_settings(
            {
                "channels": {
                    "in_app": False,
                    "email": False,
                    "vk": False,
                    "max": False,
                }
            }
        )

        key = build_deduplication_key(
            user_id=self.user.id,
            notification_type=NotificationType.SECURITY,
            source_type=NotificationSourceType.SECURITY_EVENT,
            source_id="critical-settings",
        )

        notification, created = create_notification(
            recipient=self.user,
            title="Критичное событие",
            message="Важное сообщение безопасности.",
            notification_type=NotificationType.SECURITY,
            category=NotificationCategory.SECURITY,
            level=NotificationLevel.DANGER,
            source_type=NotificationSourceType.SECURITY_EVENT,
            source_id="critical-settings",
            deduplication_key=key,
        )

        self.assertTrue(created)
        self.assertIsNotNone(notification)
        self.assertIn("in_app", notification.delivery_channels)

    def test_birthday_notification_created_only_on_birthday(self) -> None:
        """
        Поздравление создаётся только в день рождения.
        """

        self.user.birth_date = date(2005, 5, 24)

        notification, created = create_birthday_notification(
            user=self.user,
            target_date=date(2026, 5, 24),
        )

        self.assertTrue(created)
        self.assertEqual(notification.notification_type, NotificationType.BIRTHDAY)
        self.assertEqual(notification.category, NotificationCategory.BIRTHDAY)
        self.assertIn("email", notification.delivery_channels)

    def test_birthday_notification_not_created_on_other_day(self) -> None:
        """
        Поздравление не создаётся в другой день.
        """

        self.user.birth_date = date(2005, 5, 24)

        notification, created = create_birthday_notification(
            user=self.user,
            target_date=date(2026, 5, 25),
        )

        self.assertIsNone(notification)
        self.assertFalse(created)

    @patch(
        "apps.notifications.services.daily_summary_services."
        "get_today_schedule_items_for_user"
    )
    def test_daily_summary_created_when_sources_exist(self, mocked_schedule) -> None:
        """
        Ежедневная сводка создаётся, если есть хотя бы один источник.
        """

        mocked_schedule.return_value = [
            {
                "id": 1,
                "title": "История",
            }
        ]

        notification, created = create_daily_summary_notification(
            user=self.user,
            target_date=date(2026, 5, 24),
        )

        self.assertTrue(created)
        self.assertEqual(notification.notification_type, NotificationType.DAILY_SUMMARY)
        self.assertIn("1 занятий", notification.message)

    def test_daily_summary_not_created_without_sources(self) -> None:
        """
        Ежедневная сводка не создаётся без задач и событий.
        """

        notification, created = create_daily_summary_notification(
            user=self.user,
            target_date=date(2026, 5, 24),
        )

        self.assertIsNone(notification)
        self.assertFalse(created)

    @patch(
        "apps.notifications.services.deadline_services."
        "get_assignment_deadlines_for_user"
    )
    def test_assignment_deadline_notifications_created(self, mocked_deadlines) -> None:
        """
        Генератор создаёт уведомления о дедлайнах.
        """

        mocked_deadlines.return_value = [
            {
                "id": 10,
                "title": "Домашняя работа по математике",
            }
        ]

        notifications = create_assignment_deadline_notifications_for_user(
            user=self.user,
            target_date=date(2026, 5, 24),
        )

        self.assertEqual(len(notifications), 3)

        types = {notification.notification_type for notification in notifications}

        self.assertIn(NotificationType.ASSIGNMENT_DUE_TODAY, types)
        self.assertIn(NotificationType.ASSIGNMENT_DUE_TOMORROW, types)
        self.assertIn(NotificationType.ASSIGNMENT_DUE_SOON, types)

    @patch(
        "apps.notifications.services.calendar_notification_services."
        "get_calendar_events_for_user"
    )
    def test_calendar_event_notification_created(self, mocked_events) -> None:
        """
        Генератор создаёт уведомление о событии календаря.
        """

        mocked_events.return_value = [
            {
                "id": 15,
                "title": "Консультация",
                "starts_at": timezone.make_aware(datetime(2026, 5, 24, 12, 0)),
            }
        ]

        notifications = create_calendar_event_notifications_for_user(
            user=self.user,
            target_date=date(2026, 5, 24),
        )

        self.assertEqual(len(notifications), 1)
        self.assertEqual(
            notifications[0].notification_type,
            NotificationType.CALENDAR_EVENT_TODAY,
        )

    @patch(
        "apps.notifications.services.note_notification_services."
        "get_note_reminders_for_user"
    )
    def test_note_reminder_notification_created(self, mocked_notes) -> None:
        """
        Генератор создаёт уведомление по заметке с напоминанием.
        """

        starts_at = timezone.make_aware(datetime(2026, 5, 24, 10, 0))
        ends_at = timezone.make_aware(datetime(2026, 5, 24, 10, 15))

        mocked_notes.return_value = [
            {
                "id": 20,
                "title": "Позвонить куратору",
                "remind_at": starts_at,
            }
        ]

        notifications = create_note_reminder_notifications_for_user(
            user=self.user,
            starts_at=starts_at,
            ends_at=ends_at,
        )

        self.assertEqual(len(notifications), 1)
        self.assertEqual(
            notifications[0].notification_type,
            NotificationType.NOTE_REMINDER,
        )
