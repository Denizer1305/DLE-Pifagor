from __future__ import annotations

from apps.backoffice.selectors.users import get_actor_backoffice_admin_roles_queryset
from apps.backoffice.services.users.roles.payloads import (
    BackofficeRoleAssignmentPayload,
)
from apps.core.permissions import is_superadmin
from apps.core.selectors import get_object_or_none
from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.constants.roles import ORGANIZATION_ADMIN_ROLE_CODES, RoleCode
from apps.users.models import Role, User, UserRole
from rest_framework.exceptions import ValidationError


def get_role_for_backoffice_assignment(*, role_id: int) -> Role:
    """
    Возвращает активную роль для административного назначения.
    """

    role = get_object_or_none(
        Role.objects.filter(is_active=True),
        id=role_id,
    )

    if role is None:
        raise ValidationError(
            {
                "role_id": "Роль не найдена или отключена.",
            }
        )

    return role


def actor_has_backoffice_organization_scope(
    *,
    actor,
    organization_id: int | None = None,
) -> bool:
    """
    Проверяет, есть ли у администратора доступ к организации.
    """

    if not organization_id:
        return False

    if is_superadmin(actor):
        return True

    return (
        get_actor_backoffice_admin_roles_queryset(actor=actor)
        .filter(
            status=UserRoleStatus.ACTIVE,
            organization_id=organization_id,
            role__code__in=ORGANIZATION_ADMIN_ROLE_CODES,
        )
        .exists()
    )


def actor_has_backoffice_department_scope(
    *,
    actor,
    department_id: int | None = None,
) -> bool:
    """
    Проверяет, есть ли у администратора доступ к отделению.
    """

    if not department_id:
        return False

    if is_superadmin(actor):
        return True

    return (
        get_actor_backoffice_admin_roles_queryset(actor=actor)
        .filter(
            status=UserRoleStatus.ACTIVE,
            department_id=department_id,
            role__code=RoleCode.DEPARTMENT_HEAD,
        )
        .exists()
    )


def get_existing_backoffice_user_role_for_assignment(
    *,
    target_user: User,
    role: Role,
    payload: BackofficeRoleAssignmentPayload,
) -> UserRole | None:
    """
    Ищет существующее назначение роли пользователя в том же контексте.
    """

    return UserRole.objects.filter(
        user=target_user,
        role=role,
        organization_id=payload.organization_id,
        department_id=payload.department_id,
        group_id=payload.group_id,
    ).first()


def get_backoffice_user_role_for_revoke(
    *,
    target_user: User,
    user_role_id: int,
) -> UserRole | None:
    """
    Возвращает назначенную роль пользователя для отзыва.
    """

    return get_object_or_none(
        UserRole.objects.select_related(
            "role",
            "organization",
            "department",
            "group",
        ),
        id=user_role_id,
        user=target_user,
    )


# Совместимые alias'ы.
get_role_for_assignment = get_role_for_backoffice_assignment
actor_has_organization_scope = actor_has_backoffice_organization_scope
actor_has_department_scope = actor_has_backoffice_department_scope
get_existing_user_role_for_assignment = get_existing_backoffice_user_role_for_assignment
