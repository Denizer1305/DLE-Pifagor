"""
Celery-задачи приложения notifications.

Задачи отвечают за плановую генерацию уведомлений:
ежедневные сводки, дни рождения, дедлайны, просрочки, календарные события,
напоминания заметок и очистку старых уведомлений.
"""

from __future__ import annotations

from datetime import timedelta

from apps.notifications.constants import (
    DAILY_NOTIFICATION_HOUR,
    DAILY_NOTIFICATION_MINUTE,
    OVERDUE_NOTIFICATION_HOUR,
    OVERDUE_NOTIFICATION_MINUTE,
    REMINDER_SCAN_INTERVAL_MINUTES,
)
from apps.notifications.services import (
    bootstrap_notifications_for_user,
    cleanup_expired_notifications,
    create_assignment_deadline_notifications_for_user,
    create_assignment_overdue_notifications_for_user,
    create_birthday_notification,
    create_calendar_event_notifications_for_user,
    create_daily_summary_notification,
    create_note_reminder_notifications_for_user,
)
from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@shared_task(
    name="notifications.generate_daily_notifications",
)
def generate_daily_notifications(target_date: str | None = None) -> dict:
    """
    Генерирует ежедневные уведомления для всех активных пользователей.

    Включает:
    - ежедневную сводку;
    - поздравление с днём рождения;
    - дедлайны сегодня/завтра/через 3 дня;
    - события календаря на сегодня.

    target_date передаётся строкой YYYY-MM-DD, чтобы задачу можно было
    безопасно вызывать из Celery Beat и вручную.
    """

    date = parse_task_date(target_date)
    counters = create_empty_task_counters()

    for user in get_active_users_queryset():
        birthday_notification, birthday_created = create_birthday_notification(
            user=user,
            target_date=date,
        )
        counters["birthday_created"] += int(
            birthday_created and birthday_notification is not None
        )

        daily_summary_notification, daily_summary_created = (
            create_daily_summary_notification(
                user=user,
                target_date=date,
            )
        )
        counters["daily_summary_created"] += int(
            daily_summary_created and daily_summary_notification is not None
        )

        deadline_notifications = create_assignment_deadline_notifications_for_user(
            user=user,
            target_date=date,
        )
        counters["deadline_created"] += len(deadline_notifications)

        calendar_notifications = create_calendar_event_notifications_for_user(
            user=user,
            target_date=date,
        )
        counters["calendar_created"] += len(calendar_notifications)

        counters["processed_users"] += 1

    counters["target_date"] = date.isoformat()

    return counters


@shared_task(
    name="notifications.generate_overdue_notifications",
)
def generate_overdue_notifications(target_date: str | None = None) -> dict:
    """
    Генерирует уведомления о просроченных заданиях.

    По правилу проекта просрочка создаётся после полуночи следующего дня.
    Например, если задание было до 21 мая 00:00, уведомление о просрочке
    появляется 22 мая в 00:01.
    """

    date = parse_task_date(target_date)
    created_count = 0
    processed_users = 0

    for user in get_active_users_queryset():
        notifications = create_assignment_overdue_notifications_for_user(
            user=user,
            target_date=date,
        )

        created_count += len(notifications)
        processed_users += 1

    return {
        "target_date": date.isoformat(),
        "processed_users": processed_users,
        "overdue_created": created_count,
    }


@shared_task(
    name="notifications.generate_note_reminder_notifications",
)
def generate_note_reminder_notifications() -> dict:
    """
    Генерирует уведомления по заметкам с remind_at.

    Задача должна выполняться каждые REMINDER_SCAN_INTERVAL_MINUTES минут.
    """

    starts_at = timezone.now()
    ends_at = starts_at + timedelta(minutes=REMINDER_SCAN_INTERVAL_MINUTES)

    created_count = 0
    processed_users = 0

    for user in get_active_users_queryset():
        notifications = create_note_reminder_notifications_for_user(
            user=user,
            starts_at=starts_at,
            ends_at=ends_at,
        )

        created_count += len(notifications)
        processed_users += 1

    return {
        "starts_at": starts_at.isoformat(),
        "ends_at": ends_at.isoformat(),
        "processed_users": processed_users,
        "note_reminders_created": created_count,
    }


@shared_task(
    name="notifications.bootstrap_user_notifications",
)
def bootstrap_user_notifications(
    user_id: int,
    target_date: str | None = None,
) -> dict:
    """
    Celery-обёртка bootstrap-синхронизации для одного пользователя.
    """

    user = User.objects.get(id=user_id)
    date = parse_task_date(target_date)

    return bootstrap_notifications_for_user(
        user=user,
        target_date=date,
    )


@shared_task(
    name="notifications.cleanup_expired_notifications",
)
def cleanup_expired_notifications_task() -> dict:
    """
    Удаляет уведомления, у которых истёк срок хранения.
    """

    deleted_count = cleanup_expired_notifications()

    return {
        "deleted_count": deleted_count,
    }


@shared_task(
    name="notifications.generate_calendar_event_notifications",
)
def generate_calendar_event_notifications(target_date: str | None = None) -> dict:
    """
    Генерирует уведомления по событиям календаря для всех активных пользователей.

    Обычно это уже входит в daily notifications, но отдельная задача полезна
    для ручного запуска или дополнительного расписания.
    """

    date = parse_task_date(target_date)
    created_count = 0
    processed_users = 0

    for user in get_active_users_queryset():
        notifications = create_calendar_event_notifications_for_user(
            user=user,
            target_date=date,
        )

        created_count += len(notifications)
        processed_users += 1

    return {
        "target_date": date.isoformat(),
        "processed_users": processed_users,
        "calendar_created": created_count,
    }


@shared_task(
    name="notifications.generate_birthday_notifications",
)
def generate_birthday_notifications(target_date: str | None = None) -> dict:
    """
    Генерирует поздравления с днём рождения для всех активных пользователей.
    """

    date = parse_task_date(target_date)
    created_count = 0
    processed_users = 0

    for user in get_active_users_queryset():
        notification, created = create_birthday_notification(
            user=user,
            target_date=date,
        )

        created_count += int(created and notification is not None)
        processed_users += 1

    return {
        "target_date": date.isoformat(),
        "processed_users": processed_users,
        "birthday_created": created_count,
    }


def get_active_users_queryset():
    """
    Возвращает queryset активных пользователей для генерации уведомлений.
    """

    return User.objects.filter(is_active=True).order_by("id")


def parse_task_date(value: str | None):
    """
    Преобразует строковую дату YYYY-MM-DD в date.

    Если дата не передана, возвращает текущую локальную дату.
    """

    if not value:
        return timezone.localdate()

    return timezone.datetime.strptime(value, "%Y-%m-%d").date()


def create_empty_task_counters() -> dict:
    """
    Возвращает стартовые счётчики задачи генерации уведомлений.
    """

    return {
        "processed_users": 0,
        "birthday_created": 0,
        "daily_summary_created": 0,
        "deadline_created": 0,
        "calendar_created": 0,
    }


def get_daily_notification_schedule() -> dict:
    """
    Возвращает настройки расписания ежедневных уведомлений.

    Функция используется как единая точка правды для Celery Beat.
    """

    return {
        "hour": DAILY_NOTIFICATION_HOUR,
        "minute": DAILY_NOTIFICATION_MINUTE,
    }


def get_overdue_notification_schedule() -> dict:
    """
    Возвращает настройки расписания просроченных уведомлений.
    """

    return {
        "hour": OVERDUE_NOTIFICATION_HOUR,
        "minute": OVERDUE_NOTIFICATION_MINUTE,
    }
