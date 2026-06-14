from __future__ import annotations

from apps.backoffice.constants import BackofficeUserMessage
from apps.backoffice.selectors.users import actor_can_access_backoffice_user
from apps.backoffice.services.users.roles.payloads import (
    BackofficeRoleAssignmentPayload,
)
from apps.backoffice.services.users.roles.queries import (
    actor_has_backoffice_department_scope,
    actor_has_backoffice_organization_scope,
)
from apps.core.permissions import is_superadmin
from apps.users.constants.lifecycle import UserStatus
from apps.users.constants.roles import PLATFORM_ADMIN_ROLE_CODES, RoleCode
from apps.users.models import Role, User, UserRole
from rest_framework.exceptions import PermissionDenied, ValidationError

PROTECTED_BACKOFFICE_ROLE_CODES = {
    RoleCode.SUPERADMIN,
    RoleCode.PLATFORM_ADMIN,
    RoleCode.DIRECTOR,
    RoleCode.ORG_ADMIN,
}
"""
Роли, которые нельзя свободно назначать администраторам организации.

Эти роли должны назначаться только суперадминистратором платформы.
"""


def validate_target_user_can_receive_backoffice_roles(
    *,
    target_user: User,
) -> None:
    """
    Проверяет, можно ли менять роли пользователя.
    """

    if target_user.status == UserStatus.ANONYMIZED or target_user.anonymized_at:
        raise ValidationError(
            {
                "user": "Нельзя менять роли анонимизированного пользователя.",
            }
        )

    if (
        target_user.status == UserStatus.SCHEDULED_FOR_DELETION
        or target_user.scheduled_for_deletion_at
    ):
        raise ValidationError(
            {
                "user": (
                    "Нельзя менять роли пользователя, который запланирован "
                    "к удалению."
                )
            }
        )


def validate_actor_can_manage_backoffice_target_roles(
    *,
    actor,
    target_user: User,
) -> None:
    """
    Проверяет общий доступ администратора к управлению ролями пользователя.
    """

    if not actor_can_access_backoffice_user(
        actor=actor,
        target_user=target_user,
    ):
        raise PermissionDenied(BackofficeUserMessage.USER_NOT_FOUND_OR_FORBIDDEN)

    if actor and target_user and actor.id == target_user.id:
        raise ValidationError(
            {
                "user": (
                    "Администратор не может изменять собственные роли "
                    "через массовое или административное управление."
                )
            }
        )


def validate_actor_can_assign_backoffice_role(
    *,
    actor,
    role: Role,
    payload: BackofficeRoleAssignmentPayload,
) -> None:
    """
    Проверяет, может ли администратор назначить роль в указанном контексте.
    """

    if is_superadmin(actor):
        return

    if (
        role.code in PROTECTED_BACKOFFICE_ROLE_CODES
        or role.code in PLATFORM_ADMIN_ROLE_CODES
    ):
        raise PermissionDenied(
            "Только суперадминистратор может назначать "
            "административные роли платформы."
        )

    if not payload.organization_id:
        raise ValidationError(
            {
                "organization_id": (
                    "Для назначения роли администратором организации "
                    "нужно указать организацию."
                )
            }
        )

    if payload.department_id:
        if actor_has_backoffice_department_scope(
            actor=actor,
            department_id=payload.department_id,
        ):
            return

    if actor_has_backoffice_organization_scope(
        actor=actor,
        organization_id=payload.organization_id,
    ):
        return

    raise PermissionDenied(
        "У администратора нет прав назначать роль в указанном контексте."
    )


def validate_actor_can_revoke_backoffice_user_role(
    *,
    actor,
    user_role: UserRole,
) -> None:
    """
    Проверяет, может ли администратор отозвать назначенную роль.
    """

    if is_superadmin(actor):
        return

    role_code = user_role.role.code

    if (
        role_code in PROTECTED_BACKOFFICE_ROLE_CODES
        or role_code in PLATFORM_ADMIN_ROLE_CODES
    ):
        raise PermissionDenied(
            "Только суперадминистратор может отзывать "
            "административные роли платформы."
        )

    if user_role.department_id:
        if actor_has_backoffice_department_scope(
            actor=actor,
            department_id=user_role.department_id,
        ):
            return

    if user_role.organization_id:
        if actor_has_backoffice_organization_scope(
            actor=actor,
            organization_id=user_role.organization_id,
        ):
            return

    raise PermissionDenied(
        "У администратора нет прав отзывать роль в указанном контексте."
    )


# Совместимые alias'ы.
validate_target_user_can_receive_roles = (
    validate_target_user_can_receive_backoffice_roles
)
validate_actor_can_manage_target_roles = (
    validate_actor_can_manage_backoffice_target_roles
)
validate_actor_can_assign_role = validate_actor_can_assign_backoffice_role
validate_actor_can_revoke_user_role = validate_actor_can_revoke_backoffice_user_role
PROTECTED_ADMIN_ROLE_CODES = PROTECTED_BACKOFFICE_ROLE_CODES
