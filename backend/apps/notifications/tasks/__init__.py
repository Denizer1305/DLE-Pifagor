"""
Публичный интерфейс Celery-задач приложения notifications.
"""

from __future__ import annotations

from apps.notifications.tasks.notification_tasks import (
    bootstrap_user_notifications,
    cleanup_expired_notifications_task,
    generate_birthday_notifications,
    generate_calendar_event_notifications,
    generate_daily_notifications,
    generate_note_reminder_notifications,
    generate_overdue_notifications,
    get_daily_notification_schedule,
    get_overdue_notification_schedule,
)

__all__ = [
    "bootstrap_user_notifications",
    "cleanup_expired_notifications_task",
    "generate_birthday_notifications",
    "generate_calendar_event_notifications",
    "generate_daily_notifications",
    "generate_note_reminder_notifications",
    "generate_overdue_notifications",
    "get_daily_notification_schedule",
    "get_overdue_notification_schedule",
]
