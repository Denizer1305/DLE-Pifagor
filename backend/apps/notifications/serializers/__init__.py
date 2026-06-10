"""
Публичный интерфейс сериализаторов приложения notifications.
"""

from __future__ import annotations

from apps.notifications.serializers.notification_serializers import (
    NotificationActionResponseSerializer,
    NotificationBootstrapRequestSerializer,
    NotificationBootstrapResponseSerializer,
    NotificationBulkActionResponseSerializer,
    NotificationCompleteResponseSerializer,
    NotificationDeleteResponseSerializer,
    NotificationDetailSerializer,
    NotificationFeedSerializer,
    NotificationListSerializer,
    NotificationQuerySerializer,
    NotificationRecipientSerializer,
    NotificationUnreadCountSerializer,
)

__all__ = [
    "NotificationActionResponseSerializer",
    "NotificationBootstrapRequestSerializer",
    "NotificationBootstrapResponseSerializer",
    "NotificationBulkActionResponseSerializer",
    "NotificationCompleteResponseSerializer",
    "NotificationDeleteResponseSerializer",
    "NotificationDetailSerializer",
    "NotificationFeedSerializer",
    "NotificationListSerializer",
    "NotificationQuerySerializer",
    "NotificationRecipientSerializer",
    "NotificationUnreadCountSerializer",
]
