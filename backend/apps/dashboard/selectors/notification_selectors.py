from __future__ import annotations

from apps.notifications.constants import NotificationLevel, NotificationStatus
from apps.notifications.selectors import (
    get_user_notifications_queryset,
    get_user_unread_notifications_count,
)

NOTIFICATION_ICONS = {
    NotificationLevel.DANGER: "fas fa-triangle-exclamation",
    NotificationLevel.WARNING: "fas fa-circle-exclamation",
    NotificationLevel.SUCCESS: "fas fa-circle-check",
}


def get_dashboard_notifications_payload(user, limit: int = 4) -> list[dict]:
    """Returns visible user notifications shaped for dashboard panels."""

    notifications = get_user_notifications_queryset(user)[:limit]

    return [
        {
            "id": str(notification.id),
            "icon": NOTIFICATION_ICONS.get(notification.level, "fas fa-bell"),
            "title": notification.title,
            "text": notification.message,
            "is_new": notification.status == NotificationStatus.UNREAD,
        }
        for notification in notifications
    ]


def get_dashboard_unread_notifications_count(user) -> int:
    """Returns the unread count displayed in dashboard summary cards."""

    return get_user_unread_notifications_count(user)
