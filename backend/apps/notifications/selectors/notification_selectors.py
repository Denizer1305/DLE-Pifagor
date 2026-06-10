"""
Selectors уведомлений.

Файл содержит функции чтения уведомлений из базы данных.
Selectors не изменяют данные, а только возвращают queryset или отдельные значения.
"""

from __future__ import annotations

from apps.notifications.constants import NotificationStatus
from apps.notifications.models import Notification
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404


def get_user_notifications_queryset(user) -> QuerySet[Notification]:
    """
    Возвращает базовый queryset уведомлений пользователя.
    """

    return Notification.objects.for_user_feed(user)


def get_user_unread_notifications_queryset(user) -> QuerySet[Notification]:
    """
    Возвращает непрочитанные уведомления пользователя.
    """

    return Notification.objects.unread_for_user(user)


def get_user_unread_notifications_count(user) -> int:
    """
    Возвращает количество непрочитанных уведомлений пользователя.
    """

    return Notification.objects.unread_count_for_user(user)


def get_user_notification_by_id(*, user, notification_id: int) -> Notification:
    """
    Возвращает уведомление пользователя по ID.

    Если уведомление не принадлежит пользователю, будет выброшен DoesNotExist.
    """

    return get_object_or_404(
        Notification.objects.for_user(user),
        id=notification_id,
    )


def get_user_active_notification_by_id(*, user, notification_id: int) -> Notification:
    """
    Возвращает активное уведомление пользователя по ID.
    """

    return get_object_or_404(
        Notification.objects.for_user(user).visible(),
        id=notification_id,
    )


def get_notification_by_deduplication_key(
    deduplication_key: str,
) -> Notification | None:
    """
    Возвращает уведомление по ключу дедупликации.
    """

    return Notification.objects.find_by_deduplication_key(deduplication_key)


def notification_exists_by_deduplication_key(deduplication_key: str) -> bool:
    """
    Проверяет существование уведомления по ключу дедупликации.
    """

    return Notification.objects.exists_by_deduplication_key(deduplication_key)


def get_expired_notifications_queryset() -> QuerySet[Notification]:
    """
    Возвращает уведомления, срок хранения которых истёк.
    """

    return Notification.objects.expired_for_cleanup()


def get_user_notifications_by_status(
    *,
    user,
    status: str,
) -> QuerySet[Notification]:
    """
    Возвращает уведомления пользователя по статусу.
    """

    return Notification.objects.for_user(user).visible().by_status(status)


def get_user_read_notifications_queryset(user) -> QuerySet[Notification]:
    """
    Возвращает прочитанные уведомления пользователя.
    """

    return (
        Notification.objects.for_user(user)
        .visible()
        .by_status(
            NotificationStatus.READ,
        )
    )


def get_user_completed_notifications_queryset(user) -> QuerySet[Notification]:
    """
    Возвращает выполненные уведомления пользователя.
    """

    return (
        Notification.objects.for_user(user)
        .visible()
        .by_status(
            NotificationStatus.COMPLETED,
        )
    )
