"""
Публичный интерфейс selectors приложения notifications.
"""

from __future__ import annotations

from apps.notifications.selectors.notification_selectors import (
    get_expired_notifications_queryset,
    get_notification_by_deduplication_key,
    get_user_active_notification_by_id,
    get_user_completed_notifications_queryset,
    get_user_notification_by_id,
    get_user_notifications_by_status,
    get_user_notifications_queryset,
    get_user_read_notifications_queryset,
    get_user_unread_notifications_count,
    get_user_unread_notifications_queryset,
    notification_exists_by_deduplication_key,
)
from apps.notifications.selectors.source_selectors import (
    get_assignment_deadlines_for_user,
    get_calendar_events_for_user,
    get_moderation_requests_for_admin,
    get_note_reminders_for_user,
    get_support_requests_for_admin,
    get_today_schedule_items_for_user,
    get_work_to_check_for_teacher,
)

__all__ = [
    "get_assignment_deadlines_for_user",
    "get_calendar_events_for_user",
    "get_expired_notifications_queryset",
    "get_moderation_requests_for_admin",
    "get_note_reminders_for_user",
    "get_notification_by_deduplication_key",
    "get_support_requests_for_admin",
    "get_today_schedule_items_for_user",
    "get_user_active_notification_by_id",
    "get_user_completed_notifications_queryset",
    "get_user_notification_by_id",
    "get_user_notifications_by_status",
    "get_user_notifications_queryset",
    "get_user_read_notifications_queryset",
    "get_user_unread_notifications_count",
    "get_user_unread_notifications_queryset",
    "get_work_to_check_for_teacher",
    "notification_exists_by_deduplication_key",
]
