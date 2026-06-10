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
from apps.users.constants.roles import ROLE_LABELS, RoleCode
from django.utils import timezone


def get_student_dashboard_summary(*, user, request=None) -> dict:
    today = timezone.localdate()
    unread_notifications = get_dashboard_unread_notifications_count(user)

    return {
        "profile": get_student_profile_payload(user, request=request),
        "stats": get_student_stats_payload(),
        "day_stats": {
            "lessons": 0,
            "assignments": 0,
            "notifications": unread_notifications,
        },
        "schedule": [],
        "calendar": build_student_calendar_payload(today),
        "courses": [],
        "assignments": [],
        "activity_items": [],
        "grade_rows": [],
        "goals": [],
        "notifications": get_dashboard_notifications_payload(user),
        "notes": [],
    }


def get_student_profile_payload(user, request=None) -> dict:
    learner_profile = getattr(user, "learner_profile", None)
    group_label = "Личное пространство студента"

    if learner_profile:
        if learner_profile.group:
            group_label = str(learner_profile.group)
        elif learner_profile.organization:
            group_label = str(learner_profile.organization)

    return {
        "id": user.id,
        "full_name": user.get_full_name() or user.email,
        "email": user.email,
        "avatar_url": get_user_avatar_url(user, request=request),
        "role_label": ROLE_LABELS.get(RoleCode.LEARNER, "Студент"),
        "group_label": group_label,
    }


def get_student_stats_payload() -> list[dict]:
    return [
        {
            "key": "courses",
            "label": "Активные курсы",
            "value": 0,
            "caption": "Данные пока не добавлены",
            "icon": "fas fa-book-open",
            "progress": 0,
            "tone": "primary",
        },
        {
            "key": "assignments",
            "label": "Задания",
            "value": 0,
            "caption": "Данные пока не добавлены",
            "icon": "fas fa-clipboard-check",
            "progress": 0,
            "tone": "warning",
        },
        {
            "key": "average_grade",
            "label": "Средний балл",
            "value": "—",
            "caption": "Данные пока не добавлены",
            "icon": "fas fa-star",
            "progress": 0,
            "tone": "success",
        },
        {
            "key": "progress",
            "label": "Прогресс",
            "value": "0%",
            "caption": "Данные пока не добавлены",
            "icon": "fas fa-chart-line",
            "progress": 0,
            "tone": "primary",
        },
    ]


def build_student_calendar_payload(target_date) -> dict:
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
