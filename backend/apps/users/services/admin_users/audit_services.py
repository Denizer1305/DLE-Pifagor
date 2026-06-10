from __future__ import annotations

from typing import Any

from apps.users.constants.audit import AuditActorType, UserAuditAction
from apps.users.services.audit_services import create_user_audit_log

ADMIN_USERS_AUDIT_SOURCE = "admin_users"
"""
Источник аудита для административного управления пользователями.

Используется в metadata, чтобы отличать обычные пользовательские действия
от действий администратора в разделе управления пользователями.
"""


def build_admin_audit_metadata(
    *,
    metadata: dict[str, Any] | None = None,
    reason: str = "",
    bulk_action_id: str = "",
) -> dict[str, Any]:
    """
    Собирает metadata для административного аудита пользователей.

    Args:
        metadata:
            Дополнительные данные события.
        reason:
            Причина действия администратора.
        bulk_action_id:
            ID массового действия, если событие было частью bulk-операции.

    Returns:
        dict[str, Any]: Метаданные аудита.
    """

    audit_metadata = {
        "source": ADMIN_USERS_AUDIT_SOURCE,
    }

    if reason:
        audit_metadata["reason"] = reason

    if bulk_action_id:
        audit_metadata["bulk_action_id"] = bulk_action_id

    if metadata:
        audit_metadata.update(metadata)

    return audit_metadata


def create_admin_user_audit_log(
    *,
    action: str,
    actor,
    target_user,
    message: str = "",
    reason: str = "",
    metadata: dict[str, Any] | None = None,
    bulk_action_id: str = "",
    request=None,
):
    """
    Создаёт запись аудита административного действия над пользователем.

    Args:
        action:
            Код действия аудита.
        actor:
            Администратор, который выполнил действие.
        target_user:
            Пользователь, над которым выполнено действие.
        message:
            Человекочитаемое описание действия.
        reason:
            Причина действия администратора.
        metadata:
            Дополнительные данные.
        bulk_action_id:
            ID массового действия.
        request:
            HTTP-запрос.

    Returns:
        UserAuditLog: Созданная запись аудита.
    """

    return create_user_audit_log(
        action=action,
        actor=actor,
        target_user=target_user,
        actor_type=AuditActorType.ADMIN,
        message=message,
        metadata=build_admin_audit_metadata(
            metadata=metadata,
            reason=reason,
            bulk_action_id=bulk_action_id,
        ),
        request=request,
    )


def log_admin_user_updated(
    *,
    actor,
    target_user,
    changed_fields: list[str],
    reason: str = "",
    request=None,
):
    """
    Фиксирует административное обновление пользователя.

    Args:
        actor:
            Администратор, который изменил пользователя.
        target_user:
            Изменённый пользователь.
        changed_fields:
            Список изменённых полей.
        reason:
            Причина изменения.
        request:
            HTTP-запрос.

    Returns:
        UserAuditLog: Запись аудита.
    """

    return create_admin_user_audit_log(
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


def log_admin_user_email_changed(
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

    Важно:
        Отдельного UserAuditAction для смены email пока нет,
        поэтому используется PROFILE_UPDATED с расширенными metadata.

    Args:
        actor:
            Администратор, который изменил email.
        target_user:
            Пользователь, которому изменили email.
        old_email:
            Старый email.
        new_email:
            Новый email.
        reason:
            Причина изменения.
        request:
            HTTP-запрос.

    Returns:
        UserAuditLog: Запись аудита.
    """

    return create_admin_user_audit_log(
        action=UserAuditAction.PROFILE_UPDATED,
        actor=actor,
        target_user=target_user,
        message="Администратор изменил email пользователя.",
        reason=reason,
        metadata={
            "changed_fields": ["email", "is_email_verified", "email_verified_at"],
            "old_email": old_email,
            "new_email": new_email,
            "email_verification_required": True,
        },
        request=request,
    )


def log_admin_user_blocked(
    *,
    actor,
    target_user,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
):
    """
    Фиксирует административную блокировку пользователя.

    Args:
        actor:
            Администратор.
        target_user:
            Заблокированный пользователь.
        reason:
            Причина блокировки.
        bulk_action_id:
            ID массового действия.
        request:
            HTTP-запрос.

    Returns:
        UserAuditLog: Запись аудита.
    """

    return create_admin_user_audit_log(
        action=UserAuditAction.USER_BLOCKED,
        actor=actor,
        target_user=target_user,
        message=reason or "Администратор заблокировал пользователя.",
        reason=reason,
        bulk_action_id=bulk_action_id,
        request=request,
    )


def log_admin_user_unblocked(
    *,
    actor,
    target_user,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
):
    """
    Фиксирует административную разблокировку пользователя.

    Args:
        actor:
            Администратор.
        target_user:
            Разблокированный пользователь.
        reason:
            Причина разблокировки.
        bulk_action_id:
            ID массового действия.
        request:
            HTTP-запрос.

    Returns:
        UserAuditLog: Запись аудита.
    """

    return create_admin_user_audit_log(
        action=UserAuditAction.USER_UNBLOCKED,
        actor=actor,
        target_user=target_user,
        message=reason or "Администратор разблокировал пользователя.",
        reason=reason,
        bulk_action_id=bulk_action_id,
        request=request,
    )


def log_admin_user_archived(
    *,
    actor,
    target_user,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
):
    """
    Фиксирует административную архивацию пользователя.

    Args:
        actor:
            Администратор.
        target_user:
            Архивированный пользователь.
        reason:
            Причина архивации.
        bulk_action_id:
            ID массового действия.
        request:
            HTTP-запрос.

    Returns:
        UserAuditLog: Запись аудита.
    """

    return create_admin_user_audit_log(
        action=UserAuditAction.USER_ARCHIVED,
        actor=actor,
        target_user=target_user,
        message=reason or "Администратор архивировал пользователя.",
        reason=reason,
        bulk_action_id=bulk_action_id,
        request=request,
    )


def log_admin_user_restored(
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

    Args:
        actor:
            Администратор.
        target_user:
            Восстановленный пользователь.
        previous_status:
            Статус пользователя до восстановления.
        reason:
            Причина восстановления.
        bulk_action_id:
            ID массового действия.
        request:
            HTTP-запрос.

    Returns:
        UserAuditLog: Запись аудита.
    """

    return create_admin_user_audit_log(
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


def log_admin_user_scheduled_for_deletion(
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

    Args:
        actor:
            Администратор.
        target_user:
            Пользователь, запланированный к удалению.
        scheduled_for_deletion_at:
            Дата и время будущего удаления или анонимизации.
        reason:
            Причина удаления.
        bulk_action_id:
            ID массового действия.
        request:
            HTTP-запрос.

    Returns:
        UserAuditLog: Запись аудита.
    """

    return create_admin_user_audit_log(
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


def log_admin_user_roles_changed(
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

    Args:
        actor:
            Администратор.
        target_user:
            Пользователь, которому изменили роли.
        assigned_role_ids:
            ID назначенных ролей.
        revoked_user_role_ids:
            ID отозванных назначений ролей пользователя.
        reason:
            Причина изменения.
        bulk_action_id:
            ID массового действия.
        request:
            HTTP-запрос.

    Returns:
        UserAuditLog: Запись аудита.
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

    return create_admin_user_audit_log(
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
