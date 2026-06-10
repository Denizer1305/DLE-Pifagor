"""
Публичный интерфейс сервисов приложения notifications.
"""

from __future__ import annotations

from apps.notifications.services.birthday_services import create_birthday_notification
from apps.notifications.services.bootstrap_services import (
    bootstrap_notifications_for_user,
)
from apps.notifications.services.calendar_notification_services import (
    create_calendar_event_notification,
    create_calendar_event_notifications_for_user,
)
from apps.notifications.services.cleanup_services import cleanup_expired_notifications
from apps.notifications.services.daily_summary_services import (
    build_daily_summary_message,
    build_daily_summary_payload,
    create_daily_summary_notification,
)
from apps.notifications.services.deadline_services import (
    create_assignment_deadline_notification,
    create_assignment_deadline_notifications_for_user,
    create_assignment_overdue_notification,
    create_assignment_overdue_notifications_for_user,
)
from apps.notifications.services.delivery_services import (
    deliver_notification_in_app,
    mark_delivery_failed,
    mark_delivery_sent,
    mark_delivery_skipped,
    should_deliver_in_app,
    update_delivery_status,
)
from apps.notifications.services.note_notification_services import (
    create_note_reminder_notification,
    create_note_reminder_notifications_for_user,
)
from apps.notifications.services.notification_services import (
    archive_notification,
    build_deduplication_key,
    build_initial_delivery_statuses,
    complete_notification,
    create_notification,
    create_security_notification,
    create_system_notification,
    delete_notification,
    get_default_expiration_at,
    mark_all_notifications_as_read,
    mark_notification_as_read,
    normalize_delivery_channels,
)

__all__ = [
    "archive_notification",
    "bootstrap_notifications_for_user",
    "build_daily_summary_message",
    "build_daily_summary_payload",
    "build_deduplication_key",
    "build_initial_delivery_statuses",
    "cleanup_expired_notifications",
    "complete_notification",
    "create_assignment_deadline_notification",
    "create_assignment_deadline_notifications_for_user",
    "create_assignment_overdue_notification",
    "create_assignment_overdue_notifications_for_user",
    "create_birthday_notification",
    "create_calendar_event_notification",
    "create_calendar_event_notifications_for_user",
    "create_daily_summary_notification",
    "create_note_reminder_notification",
    "create_note_reminder_notifications_for_user",
    "create_notification",
    "create_security_notification",
    "create_system_notification",
    "delete_notification",
    "deliver_notification_in_app",
    "get_default_expiration_at",
    "mark_all_notifications_as_read",
    "mark_delivery_failed",
    "mark_delivery_sent",
    "mark_delivery_skipped",
    "mark_notification_as_read",
    "normalize_delivery_channels",
    "should_deliver_in_app",
    "update_delivery_status",
]
