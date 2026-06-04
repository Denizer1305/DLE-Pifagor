"""
Публичный интерфейс менеджеров приложения notifications.
"""

from __future__ import annotations

from apps.notifications.managers.notification_managers import (
    NotificationManager,
    NotificationQuerySet,
)

__all__ = [
    "NotificationManager",
    "NotificationQuerySet",
]
