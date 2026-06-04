"""
Сервисы очистки уведомлений.
"""

from __future__ import annotations

from apps.notifications.selectors import get_expired_notifications_queryset


def cleanup_expired_notifications() -> int:
    """
    Удаляет уведомления, у которых истёк срок хранения.

    Возвращает количество удалённых уведомлений.
    """

    queryset = get_expired_notifications_queryset()
    deleted_count, _details = queryset.delete()

    return deleted_count
