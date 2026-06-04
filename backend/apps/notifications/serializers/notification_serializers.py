"""
Фасад сериализаторов приложения notifications.

Файл не содержит собственной логики. Он переэкспортирует сериализаторы из
декомпозированных файлов, чтобы импорты во views оставались короткими.
"""

from __future__ import annotations

from apps.notifications.serializers.notification_action_serializers import (
    NotificationActionResponseSerializer,
    NotificationBulkActionResponseSerializer,
    NotificationCompleteResponseSerializer,
    NotificationDeleteResponseSerializer,
)
from apps.notifications.serializers.notification_bootstrap_serializers import (
    NotificationBootstrapRequestSerializer,
    NotificationBootstrapResponseSerializer,
)
from apps.notifications.serializers.notification_read_serializers import (
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
