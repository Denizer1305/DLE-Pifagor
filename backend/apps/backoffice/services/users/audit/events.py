from __future__ import annotations

from apps.backoffice.services.users.audit.writer import create_backoffice_user_audit_log
from apps.users.constants.audit import UserAuditAction


def log_backoffice_user_updated(
    *,
    actor,
    target_user,
    changed_fields: list[str],
    reason: str = "",
    request=None,
):
    """
    Фиксирует административное обновление пользователя.
    """

    return create_backoffice_user_audit_log(
        action=UserAuditAction.PROFILE_UPDATED,
        actor=actor,
        target_user=target_user,
        message="Администратор обновил данные пользователя.",
        reason=reason,
        metadata={
            "changed_fields": changed_fields,
        },
        request=request,
    )


def log_backoffice_user_email_changed(
    *,
    actor,
    target_user,
    old_email: str,
    new_email: str,
    reason: str = "",
    request=None,
):
    """
    Фиксирует административное изменение email пользователя.
    """

    return create_backoffice_user_audit_log(
        action=UserAuditAction.PROFILE_UPDATED,
        actor=actor,
        target_user=target_user,
        message="Администратор изменил email пользователя.",
        reason=reason,
        metadata={
            "changed_fields": [
                "email",
                "is_email_verified",
                "email_verified_at",
            ],
            "old_email": old_email,
            "new_email": new_email,
            "email_verification_required": True,
        },
        request=request,
    )


def log_backoffice_user_blocked(
    *,
    actor,
    target_user,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
):
    """
    Фиксирует административную блокировку пользователя.
    """

    return create_backoffice_user_audit_log(
        action=UserAuditAction.USER_BLOCKED,
        actor=actor,
        target_user=target_user,
        message=reason or "Администратор заблокировал пользователя.",
        reason=reason,
        bulk_action_id=bulk_action_id,
        request=request,
    )


def log_backoffice_user_unblocked(
    *,
    actor,
    target_user,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
):
    """
    Фиксирует административную разблокировку пользователя.
    """

    return create_backoffice_user_audit_log(
        action=UserAuditAction.USER_UNBLOCKED,
        actor=actor,
        target_user=target_user,
        message=reason or "Администратор разблокировал пользователя.",
        reason=reason,
        bulk_action_id=bulk_action_id,
        request=request,
    )


def log_backoffice_user_archived(
    *,
    actor,
    target_user,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
):
    """
    Фиксирует административную архивацию пользователя.
    """

    return create_backoffice_user_audit_log(
        action=UserAuditAction.USER_ARCHIVED,
        actor=actor,
        target_user=target_user,
        message=reason or "Администратор архивировал пользователя.",
        reason=reason,
        bulk_action_id=bulk_action_id,
        request=request,
    )


def log_backoffice_user_restored(
    *,
    actor,
    target_user,
    previous_status: str = "",
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
):
    """
    Фиксирует административное восстановление пользователя.
    """

    return create_backoffice_user_audit_log(
        action=UserAuditAction.USER_RESTORED,
        actor=actor,
        target_user=target_user,
        message=reason or "Администратор восстановил пользователя.",
        reason=reason,
        bulk_action_id=bulk_action_id,
        metadata={
            "previous_status": previous_status,
        },
        request=request,
    )


def log_backoffice_user_scheduled_for_deletion(
    *,
    actor,
    target_user,
    scheduled_for_deletion_at,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
):
    """
    Фиксирует административное планирование удаления пользователя.
    """

    return create_backoffice_user_audit_log(
        action=UserAuditAction.USER_SCHEDULED_FOR_DELETION,
        actor=actor,
        target_user=target_user,
        message=reason or "Администратор запланировал удаление пользователя.",
        reason=reason,
        bulk_action_id=bulk_action_id,
        metadata={
            "scheduled_for_deletion_at": (
                scheduled_for_deletion_at.isoformat()
                if scheduled_for_deletion_at
                else ""
            ),
        },
        request=request,
    )


def log_backoffice_user_roles_changed(
    *,
    actor,
    target_user,
    assigned_role_ids: list[int] | None = None,
    revoked_user_role_ids: list[int] | None = None,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
):
    """
    Фиксирует административное изменение ролей пользователя.
    """

    assigned_role_ids = assigned_role_ids or []
    revoked_user_role_ids = revoked_user_role_ids or []

    if assigned_role_ids and not revoked_user_role_ids:
        action = UserAuditAction.ROLE_ASSIGNED
        message = "Администратор назначил роли пользователю."
    elif revoked_user_role_ids and not assigned_role_ids:
        action = UserAuditAction.ROLE_REVOKED
        message = "Администратор отозвал роли пользователя."
    else:
        action = UserAuditAction.ROLE_ASSIGNED
        message = "Администратор изменил роли пользователя."

    return create_backoffice_user_audit_log(
        action=action,
        actor=actor,
        target_user=target_user,
        message=message,
        reason=reason,
        bulk_action_id=bulk_action_id,
        metadata={
            "assigned_role_ids": assigned_role_ids,
            "revoked_user_role_ids": revoked_user_role_ids,
        },
        request=request,
    )


# Совместимые alias'ы на время переноса старой admin-user логики.
log_admin_user_updated = log_backoffice_user_updated
log_admin_user_email_changed = log_backoffice_user_email_changed
log_admin_user_blocked = log_backoffice_user_blocked
log_admin_user_unblocked = log_backoffice_user_unblocked
log_admin_user_archived = log_backoffice_user_archived
log_admin_user_restored = log_backoffice_user_restored
log_admin_user_scheduled_for_deletion = log_backoffice_user_scheduled_for_deletion
log_admin_user_roles_changed = log_backoffice_user_roles_changed
