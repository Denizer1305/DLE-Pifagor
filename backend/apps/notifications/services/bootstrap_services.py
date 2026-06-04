"""
Bootstrap-сервисы уведомлений.

Bootstrap вызывается отдельной ручкой при входе пользователя в личный кабинет.
Он не должен создавать дубли. Его задача — убедиться, что важные уведомления
на текущий день существуют, даже если Celery ещё не успел их создать.
"""

from __future__ import annotations

from apps.notifications.services.birthday_services import create_birthday_notification
from apps.notifications.services.calendar_notification_services import (
    create_calendar_event_notifications_for_user,
)
from apps.notifications.services.daily_summary_services import (
    create_daily_summary_notification,
)
from apps.notifications.services.deadline_services import (
    create_assignment_deadline_notifications_for_user,
)
from apps.notifications.services.note_notification_services import (
    create_note_reminder_notifications_for_user,
)
from django.utils import timezone


def bootstrap_notifications_for_user(*, user, target_date=None) -> dict:
    """
    Синхронизирует уведомления пользователя на текущий день.

    Возвращает краткую статистику по созданным уведомлениям.
    """

    target_date = target_date or timezone.localdate()
    starts_at, ends_at = get_day_bounds(target_date)

    created_notifications = []

    birthday_notification, birthday_created = create_birthday_notification(
        user=user,
        target_date=target_date,
    )

    if birthday_created:
        created_notifications.append(birthday_notification)

    daily_summary_notification, daily_summary_created = (
        create_daily_summary_notification(
            user=user,
            target_date=target_date,
        )
    )

    if daily_summary_created:
        created_notifications.append(daily_summary_notification)

    created_notifications.extend(
        create_assignment_deadline_notifications_for_user(
            user=user,
            target_date=target_date,
        )
    )
    created_notifications.extend(
        create_calendar_event_notifications_for_user(
            user=user,
            target_date=target_date,
        )
    )
    created_notifications.extend(
        create_note_reminder_notifications_for_user(
            user=user,
            starts_at=starts_at,
            ends_at=ends_at,
        )
    )

    return {
        "target_date": target_date,
        "created_count": len(created_notifications),
        "created_ids": [
            notification.id for notification in created_notifications if notification
        ],
    }


def get_day_bounds(target_date):
    """
    Возвращает начало и конец выбранного дня.
    """

    starts_at = timezone.make_aware(
        timezone.datetime.combine(target_date, timezone.datetime.min.time()),
    )
    ends_at = timezone.make_aware(
        timezone.datetime.combine(target_date, timezone.datetime.max.time()),
    )

    return starts_at, ends_at
