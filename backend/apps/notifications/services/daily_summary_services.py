"""
Сервисы ежедневной сводки уведомлений.

Ежедневная сводка создаётся один раз в день, только если у пользователя
есть события, задачи или важные активности на выбранную дату.
"""

from __future__ import annotations

from apps.notifications.constants import (
    NotificationCategory,
    NotificationLevel,
    NotificationSourceType,
    NotificationType,
)
from apps.notifications.selectors import (
    get_assignment_deadlines_for_user,
    get_calendar_events_for_user,
    get_moderation_requests_for_admin,
    get_note_reminders_for_user,
    get_support_requests_for_admin,
    get_today_schedule_items_for_user,
    get_work_to_check_for_teacher,
)
from apps.notifications.services.notification_services import (
    build_deduplication_key,
    create_notification,
)
from django.utils import timezone


def create_daily_summary_notification(
    *, user, target_date=None
) -> tuple[object | None, bool]:
    """
    Создаёт ежедневную сводку пользователя.

    Если на выбранную дату нет событий, уведомление не создаётся.
    """

    target_date = target_date or timezone.localdate()
    summary = build_daily_summary_payload(
        user=user,
        target_date=target_date,
    )

    if not summary["total_count"]:
        return None, False

    title = "Ваш план на сегодня"
    message = build_daily_summary_message(summary)

    deduplication_key = build_deduplication_key(
        user_id=user.id,
        notification_type=NotificationType.DAILY_SUMMARY,
        source_type=NotificationSourceType.USER,
        source_id=user.id,
        target_date=target_date,
    )

    return create_notification(
        recipient=user,
        title=title,
        message=message,
        notification_type=NotificationType.DAILY_SUMMARY,
        category=NotificationCategory.DAILY_SUMMARY,
        level=NotificationLevel.INFO,
        source_type=NotificationSourceType.USER,
        source_id=str(user.id),
        deduplication_key=deduplication_key,
        action_label="Открыть расписание",
        action_url=get_daily_summary_action_url(user=user),
        payload=summary,
    )


def build_daily_summary_payload(*, user, target_date) -> dict:
    """
    Собирает данные ежедневной сводки пользователя.
    """

    starts_at, ends_at = get_day_bounds(target_date)

    schedule_items = get_today_schedule_items_for_user(
        user=user,
        target_date=target_date,
    )
    assignment_deadlines = get_assignment_deadlines_for_user(
        user=user,
        target_date=target_date,
    )
    calendar_events = get_calendar_events_for_user(
        user=user,
        target_date=target_date,
    )
    note_reminders = get_note_reminders_for_user(
        user=user,
        starts_at=starts_at,
        ends_at=ends_at,
    )
    work_to_check = get_work_to_check_for_teacher(
        user=user,
        target_date=target_date,
    )
    moderation_requests = get_moderation_requests_for_admin(
        user=user,
        target_date=target_date,
    )
    support_requests = get_support_requests_for_admin(
        user=user,
        target_date=target_date,
    )

    total_count = (
        len(schedule_items)
        + len(assignment_deadlines)
        + len(calendar_events)
        + len(note_reminders)
        + len(work_to_check)
        + len(moderation_requests)
        + len(support_requests)
    )

    return {
        "target_date": target_date.isoformat(),
        "total_count": total_count,
        "schedule_count": len(schedule_items),
        "assignment_deadline_count": len(assignment_deadlines),
        "calendar_event_count": len(calendar_events),
        "note_reminder_count": len(note_reminders),
        "work_to_check_count": len(work_to_check),
        "moderation_request_count": len(moderation_requests),
        "support_request_count": len(support_requests),
    }


def build_daily_summary_message(summary: dict) -> str:
    """
    Собирает человекочитаемый текст ежедневной сводки.
    """

    parts = []

    if summary["schedule_count"]:
        parts.append(f"{summary['schedule_count']} занятий")

    if summary["assignment_deadline_count"]:
        parts.append(f"{summary['assignment_deadline_count']} заданий к сдаче")

    if summary["calendar_event_count"]:
        parts.append(f"{summary['calendar_event_count']} событий календаря")

    if summary["note_reminder_count"]:
        parts.append(f"{summary['note_reminder_count']} напоминаний")

    if summary["work_to_check_count"]:
        parts.append(f"{summary['work_to_check_count']} работ на проверку")

    if summary["moderation_request_count"]:
        parts.append(f"{summary['moderation_request_count']} заявок на модерацию")

    if summary["support_request_count"]:
        parts.append(f"{summary['support_request_count']} обращений поддержки")

    if not parts:
        return ""

    return f"Сегодня вас ждёт: {', '.join(parts)}."


def get_daily_summary_action_url(*, user) -> str:
    """
    Возвращает ссылку действия для ежедневной сводки.
    """

    role_code = get_user_role_code(user)

    if role_code == "teacher":
        return "/teacher/schedule"

    if role_code == "learner":
        return "/student/schedule"

    if role_code == "guardian":
        return "/parent/schedule"

    return "/admin"


def get_user_role_code(user) -> str:
    """
    Возвращает активную роль пользователя для уведомлений.
    """

    settings_obj = getattr(user, "settings", None)

    if settings_obj and settings_obj.active_role:
        return settings_obj.active_role

    if user.is_superuser:
        return "admin"

    return "learner"


def get_day_bounds(target_date):
    """
    Возвращает начало и конец указанного дня в текущей timezone.
    """

    starts_at = timezone.make_aware(
        timezone.datetime.combine(target_date, timezone.datetime.min.time()),
    )
    ends_at = timezone.make_aware(
        timezone.datetime.combine(target_date, timezone.datetime.max.time()),
    )

    return starts_at, ends_at
