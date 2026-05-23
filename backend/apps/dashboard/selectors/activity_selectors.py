from __future__ import annotations

from apps.dashboard.selectors.common import get_optional_model
from apps.users.constants.onboarding import JoinRequestStatus
from apps.users.models import UserAuditLog, UserJoinRequest
from django.contrib.auth import get_user_model

User = get_user_model()


def get_recent_users_payload(limit: int = 6) -> list[dict]:
    """
    Возвращает последних зарегистрированных пользователей.
    """

    users = User.objects.order_by("-created_at").only(
        "id",
        "email",
        "first_name",
        "last_name",
        "middle_name",
        "status",
        "created_at",
    )[:limit]

    return [
        {
            "id": user.id,
            "full_name": user.get_full_name() or user.email,
            "email": user.email,
            "status": user.status,
            "created_at": user.created_at,
        }
        for user in users
    ]


def get_join_request_organization_payload(join_request) -> dict | None:
    if not join_request.organization:
        return None

    organization_name = (
        join_request.organization.short_name
        if getattr(join_request.organization, "short_name", "")
        else join_request.organization.name
    )

    return {
        "id": join_request.organization_id,
        "name": organization_name,
    }


def get_join_request_department_payload(join_request) -> dict | None:
    if not join_request.department:
        return None

    return {
        "id": join_request.department_id,
        "name": join_request.department.name,
    }


def get_join_request_group_payload(join_request) -> dict | None:
    if not join_request.group:
        return None

    return {
        "id": join_request.group_id,
        "name": join_request.group.name,
    }


def get_join_requests_payload(limit: int = 5) -> list[dict]:
    """
    Возвращает ожидающие заявки на присоединение.
    """

    queryset = (
        UserJoinRequest.objects.select_related(
            "user",
            "organization",
            "department",
            "group",
        )
        .filter(status=JoinRequestStatus.PENDING)
        .order_by("-created_at")[:limit]
    )

    return [
        {
            "id": item.id,
            "request_type": item.request_type,
            "status": item.status,
            "user": {
                "id": item.user_id,
                "full_name": item.user.get_full_name() or item.user.email,
                "email": item.user.email,
            },
            "organization": get_join_request_organization_payload(item),
            "department": get_join_request_department_payload(item),
            "group": get_join_request_group_payload(item),
            "message": item.message,
            "created_at": item.created_at,
        }
        for item in queryset
    ]


def get_feedback_requests_payload(limit: int = 5) -> list[dict]:
    """
    Возвращает последние новые обращения feedback.
    """

    FeedbackRequest = get_optional_model("feedback", "FeedbackRequest")

    if FeedbackRequest is None:
        return []

    queryset = FeedbackRequest.objects.filter(status="new").order_by("-created_at")[
        :limit
    ]

    return [
        {
            "id": item.id,
            "full_name": item.full_name,
            "email": item.email,
            "topic": item.topic,
            "status": item.status,
            "message": item.message,
            "created_at": item.created_at,
        }
        for item in queryset
    ]


def get_audit_actor_payload(user) -> dict | None:
    if not user:
        return None

    return {
        "id": user.id,
        "full_name": user.get_full_name(),
        "email": user.email,
    }


def get_audit_events_payload(limit: int = 6) -> list[dict]:
    """
    Возвращает последние события пользовательского аудита.
    """

    queryset = UserAuditLog.objects.select_related(
        "actor",
        "target_user",
    ).order_by(
        "-created_at"
    )[:limit]

    return [
        {
            "id": item.id,
            "action": item.action,
            "message": item.message,
            "actor": get_audit_actor_payload(item.actor),
            "target_user": get_audit_actor_payload(item.target_user),
            "created_at": item.created_at,
        }
        for item in queryset
    ]
