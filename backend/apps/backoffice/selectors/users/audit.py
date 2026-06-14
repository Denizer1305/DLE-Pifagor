from __future__ import annotations

from apps.backoffice.constants import BACKOFFICE_USER_AUDIT_LIMIT
from apps.backoffice.selectors.users.detail import get_backoffice_user_by_id_for_actor
from apps.users.models import UserAuditLog
from django.db.models import QuerySet


def get_backoffice_user_audit_logs_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet audit-записей пользователей.
    """

    return UserAuditLog.objects.select_related(
        "actor",
        "target_user",
    ).order_by(
        "-created_at",
        "-id",
    )


def get_backoffice_user_audit_logs_for_target(*, target_user) -> QuerySet:
    """
    Возвращает audit-записи конкретного пользователя.
    """

    if not target_user:
        return UserAuditLog.objects.none()

    return get_backoffice_user_audit_logs_queryset().filter(
        target_user=target_user,
    )


def get_backoffice_user_audit_logs_for_actor(
    *,
    actor,
    target_user_id: int,
) -> QuerySet:
    """
    Возвращает audit-записи пользователя с учётом прав администратора.
    """

    target_user = get_backoffice_user_by_id_for_actor(
        actor=actor,
        user_id=target_user_id,
    )

    if target_user is None:
        return UserAuditLog.objects.none()

    return get_backoffice_user_audit_logs_for_target(
        target_user=target_user,
    )


def get_recent_backoffice_user_audit_logs_for_target(
    *,
    target_user,
    limit: int = BACKOFFICE_USER_AUDIT_LIMIT,
) -> list[UserAuditLog]:
    """
    Возвращает последние audit-записи пользователя.
    """

    return list(
        get_backoffice_user_audit_logs_for_target(
            target_user=target_user,
        )[:limit]
    )
