from __future__ import annotations

from apps.dashboard.selectors.stats_selectors import count_feedback_new
from apps.users.constants.onboarding import JoinRequestStatus
from apps.users.models import UserJoinRequest


def get_system_health_payload() -> dict:
    """
    Формирует минимальный блок состояния системы для dashboard.
    """

    new_feedback_count = count_feedback_new()
    pending_requests_count = UserJoinRequest.objects.filter(
        status=JoinRequestStatus.PENDING,
    ).count()

    status = "ok"

    if new_feedback_count >= 10 or pending_requests_count >= 10:
        status = "warning"

    checks = [
        {
            "key": "database",
            "label": "База данных",
            "status": "ok",
            "text": "Соединение активно",
            "icon": "fas fa-database",
        },
        {
            "key": "feedback",
            "label": "Обращения",
            "status": "warning" if new_feedback_count else "ok",
            "text": f"Новых обращений: {new_feedback_count}",
            "icon": "fas fa-envelope-open-text",
        },
        {
            "key": "join_requests",
            "label": "Заявки",
            "status": "warning" if pending_requests_count else "ok",
            "text": f"Ожидают проверки: {pending_requests_count}",
            "icon": "fas fa-user-check",
        },
    ]

    return {
        "status": status,
        "checks": checks,
    }
