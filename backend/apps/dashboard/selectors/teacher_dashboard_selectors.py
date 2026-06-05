from __future__ import annotations

from datetime import timedelta

from apps.dashboard.selectors.calendar_selectors import (
    build_admin_calendar_day_payload,
    get_calendar_start_date,
    get_month_label,
)
from apps.dashboard.selectors.notification_selectors import (
    get_dashboard_notifications_payload,
    get_dashboard_unread_notifications_count,
)
from apps.dashboard.selectors.profile_selectors import get_user_avatar_url
from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.constants.roles import ROLE_LABELS, STAFF_ROLE_CODES
from django.utils import timezone


def get_teacher_dashboard_summary(*, user, request=None) -> dict:
    today = timezone.localdate()

    return {
        "profile": get_teacher_profile_payload(user, request=request),
        "stats": get_teacher_stats_payload(user),
        "schedule": [],
        "calendar": build_teacher_calendar_payload(today),
        "courses": [],
        "attention_items": [],
        "activity_items": [],
        "journal_rows": [],
        "notifications": get_dashboard_notifications_payload(user),
        "notes": [],
    }


def get_teacher_profile_payload(user, request=None) -> dict:
    role_code = get_teacher_role_code(user)
    teacher_profile = getattr(user, "teacher_profile", None)
    subject_label = ""

    if teacher_profile:
        subject_label = teacher_profile.public_title or teacher_profile.position or ""

    return {
        "id": user.id,
        "full_name": user.get_full_name() or user.email,
        "email": user.email,
        "avatar_url": get_user_avatar_url(user, request=request),
        "role_label": ROLE_LABELS.get(role_code, "Преподаватель"),
        "subject_label": subject_label or "Учебные дисциплины",
    }


def get_teacher_role_code(user):
    user_role = (
        user.user_roles.select_related("role")
        .filter(
            role__code__in=STAFF_ROLE_CODES,
            status=UserRoleStatus.ACTIVE,
            role__is_active=True,
        )
        .order_by("role__sort_order")
        .first()
    )

    if user_role:
        return user_role.role.code

    return None


def get_teacher_stats_payload(user) -> list[dict]:
    return [
        {
            "key": "courses",
            "label": "Активные курсы",
            "value": 0,
            "caption": "Курсы в работе",
            "icon": "fas fa-book-open",
            "progress": 0,
            "tone": "primary",
        },
        {
            "key": "groups",
            "label": "Группы",
            "value": 0,
            "caption": "Закрепленные группы",
            "icon": "fas fa-users",
            "progress": 0,
            "tone": "primary",
        },
        {
            "key": "checking",
            "label": "На проверке",
            "value": 0,
            "caption": "Работы ожидают проверки",
            "icon": "fas fa-clipboard-check",
            "progress": 0,
            "tone": "warning",
        },
        {
            "key": "average_grade",
            "label": "Средний балл",
            "value": "0",
            "caption": "Средний результат",
            "icon": "fas fa-star",
            "progress": 0,
            "tone": "success",
        },
        {
            "key": "homework_done",
            "label": "Домашние задания",
            "value": 0,
            "caption": "Выполнены вовремя",
            "icon": "fas fa-house-laptop",
            "progress": 0,
            "tone": "neutral",
        },
        {
            "key": "attendance",
            "label": "Посещаемость",
            "value": 0,
            "caption": "Средняя посещаемость",
            "icon": "fas fa-chart-column",
            "progress": 0,
            "tone": "primary",
        },
        {
            "key": "lessons_today",
            "label": "Занятия сегодня",
            "value": 0,
            "caption": "Запланированные пары",
            "icon": "fas fa-calendar-day",
            "progress": 0,
            "tone": "primary",
        },
        {
            "key": "notifications",
            "label": "Уведомления",
            "value": get_dashboard_unread_notifications_count(user),
            "caption": "Новые уведомления",
            "icon": "fas fa-bell",
            "progress": 0,
            "tone": "neutral",
        },
    ]


def build_teacher_calendar_payload(target_date) -> dict:
    first_day = target_date.replace(day=1)
    calendar_start = get_calendar_start_date(first_day)
    days = []

    for index in range(42):
        current_date = calendar_start + timedelta(days=index)
        day_payload = build_admin_calendar_day_payload(
            current_date=current_date,
            first_day=first_day,
            selected_date=target_date,
            today=timezone.localdate(),
        )
        day_payload["date_label"] = ""
        day_payload["title"] = ""
        day_payload["text"] = ""
        day_payload["event_types"] = []
        days.append(day_payload)

    return {
        "month_label": get_month_label(first_day),
        "selected_date": target_date.isoformat(),
        "days": days,
    }
