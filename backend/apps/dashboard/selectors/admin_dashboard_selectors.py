from __future__ import annotations

from apps.dashboard.selectors.activity_selectors import (
    get_audit_events_payload,
    get_feedback_requests_payload,
    get_join_requests_payload,
    get_recent_users_payload,
)
from apps.dashboard.selectors.calendar_selectors import build_admin_calendar_payload
from apps.dashboard.selectors.profile_selectors import get_admin_profile_payload
from apps.dashboard.selectors.quick_actions_selectors import get_quick_actions_payload
from apps.dashboard.selectors.stats_selectors import get_admin_stats_payload
from apps.dashboard.selectors.system_selectors import get_system_health_payload


def get_admin_dashboard_summary(*, user, request=None) -> dict:
    """
    Возвращает агрегированную сводку главной страницы администратора.
    """

    return {
        "profile": get_admin_profile_payload(user, request=request),
        "stats": get_admin_stats_payload(),
        "calendar": build_admin_calendar_payload(),
        "recent_users": get_recent_users_payload(),
        "join_requests": get_join_requests_payload(),
        "feedback_requests": get_feedback_requests_payload(),
        "audit_events": get_audit_events_payload(),
        "system_health": get_system_health_payload(),
        "quick_actions": get_quick_actions_payload(),
    }
