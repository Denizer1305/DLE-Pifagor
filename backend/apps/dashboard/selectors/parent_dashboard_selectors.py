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
from apps.users.constants.lifecycle import GuardianLearnerStatus
from apps.users.constants.roles import ROLE_LABELS, RoleCode
from django.utils import timezone


def get_parent_dashboard_summary(*, user, request=None) -> dict:
    today = timezone.localdate()
    notifications = get_dashboard_notifications_payload(user)
    children_count = user.guardian_learner_links.filter(
        status=GuardianLearnerStatus.ACTIVE,
    ).count()

    return {
        "profile": get_parent_profile_payload(user, request=request),
        "stats": get_parent_stats_payload(user, children_count),
        "day_stats": {
            "lessons": 0,
            "assignments": 0,
            "messages": get_dashboard_unread_notifications_count(user),
        },
        "schedule": [],
        "calendar": build_parent_calendar_payload(today),
        "courses": [],
        "important_items": map_notifications_to_important_items(notifications),
        "activity_items": [],
        "grade_rows": [],
        "messages": [],
        "notifications": notifications,
        "notes": [],
    }


def get_parent_profile_payload(user, request=None) -> dict:
    return {
        "id": user.id,
        "full_name": user.get_full_name() or user.email,
        "email": user.email,
        "avatar_url": get_user_avatar_url(user, request=request),
        "role_label": ROLE_LABELS.get(RoleCode.GUARDIAN, "Родитель"),
    }


def get_parent_stats_payload(user, children_count: int) -> list[dict]:
    unread_count = get_dashboard_unread_notifications_count(user)

    return [
        {
            "key": "children",
            "label": "Детей",
            "value": children_count,
            "caption": "Подтвержденные учебные профили",
            "icon": "fas fa-child-reaching",
            "progress": 0,
            "tone": "primary",
        },
        {
            "key": "average_grade",
            "label": "Средний балл",
            "value": "—",
            "caption": "Данные пока не добавлены",
            "icon": "fas fa-chart-line",
            "progress": 0,
            "tone": "neutral",
        },
        {
            "key": "attendance",
            "label": "Посещаемость",
            "value": "0%",
            "caption": "Данные пока не добавлены",
            "icon": "fas fa-calendar-check",
            "progress": 0,
            "tone": "neutral",
        },
        {
            "key": "messages",
            "label": "Уведомления",
            "value": unread_count,
            "caption": "Новые уведомления",
            "icon": "fas fa-bell",
            "progress": 0,
            "tone": "primary",
        },
    ]


def map_notifications_to_important_items(notifications: list[dict]) -> list[dict]:
    return [
        {
            "id": notification["id"],
            "icon": notification["icon"],
            "title": notification["title"],
            "text": notification["text"],
            "meta": "Новое" if notification["is_new"] else "",
            "tone": "primary",
        }
        for notification in notifications
    ]


def build_parent_calendar_payload(target_date) -> dict:
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
