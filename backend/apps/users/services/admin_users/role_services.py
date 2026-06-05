from __future__ import annotations

from dataclasses import dataclass

from apps.users.constants.lifecycle import UserRoleStatus, UserStatus
from apps.users.constants.roles import (
    ORGANIZATION_ADMIN_ROLE_CODES,
    PLATFORM_ADMIN_ROLE_CODES,
    RoleCode,
)
from apps.users.models import Role, User, UserRole
from apps.users.permissions.helpers import is_superadmin
from apps.users.selectors.admin_user_selectors import (
    actor_can_access_admin_user,
    get_actor_admin_roles_queryset,
)
from apps.users.services.admin_users.audit_services import log_admin_user_roles_changed
from django.db import IntegrityError, transaction
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied, ValidationError

PROTECTED_ADMIN_ROLE_CODES = {
    RoleCode.SUPERADMIN,
    RoleCode.PLATFORM_ADMIN,
    RoleCode.DIRECTOR,
    RoleCode.ORG_ADMIN,
}
"""
Роли, которые нельзя свободно назначать администраторам организации.

Эти роли должны назначаться только суперадминистратором платформы,
иначе администратор организации сможет повысить себе или другим права.
"""


@dataclass
class AdminRoleAssignmentPayload:
    """
    Нормализованные данные для назначения роли пользователю.

    Attributes:
        role_id:
            ID роли.
        organization_id:
            ID организации.
        department_id:
            ID отделения.
        group_id:
            ID группы.
    """

    role_id: int
    organization_id: int | None = None
    department_id: int | None = None
    group_id: int | None = None


def normalize_role_assignment_payload(raw_payload: dict) -> AdminRoleAssignmentPayload:
    """
    Нормализует payload назначения роли.

    Args:
        raw_payload:
            Словарь с данными роли.

    Returns:
        AdminRoleAssignmentPayload: Нормализованный payload.

    Raises:
        ValidationError: Если role_id не передан.
    """

    role_id = raw_payload.get("role_id") or raw_payload.get("role")

    if not role_id:
        raise ValidationError(
            {
                "role_id": "Необходимо указать роль.",
            }
        )

    return AdminRoleAssignmentPayload(
        role_id=int(role_id),
        organization_id=raw_payload.get("organization_id")
        or raw_payload.get("organization"),
        department_id=raw_payload.get("department_id") or raw_payload.get("department"),
        group_id=raw_payload.get("group_id") or raw_payload.get("group"),
    )


def get_role_for_assignment(*, role_id: int) -> Role:
    """
    Возвращает активную роль для назначения.

    Args:
        role_id:
            ID роли.

    Returns:
        Role: Роль.

    Raises:
        ValidationError: Если роль не найдена или отключена.
    """

    role = Role.objects.filter(
        id=role_id,
        is_active=True,
    ).first()

    if role is None:
        raise ValidationError(
            {
                "role_id": "Роль не найдена или отключена.",
            }
        )

    return role


def validate_target_user_can_receive_roles(*, target_user: User) -> None:
    """
    Проверяет, можно ли менять роли пользователя.

    Args:
        target_user:
            Пользователь, которому меняют роли.

    Raises:
        ValidationError: Если роли менять нельзя.
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


def validate_actor_can_manage_target_roles(*, actor, target_user: User) -> None:
    """
    Проверяет общий доступ администратора к управлению ролями пользователя.

    Args:
        actor:
            Администратор.
        target_user:
            Целевой пользователь.

    Raises:
        PermissionDenied: Если пользователь недоступен.
        ValidationError: Если администратор меняет свои роли.
    """

    if not actor_can_access_admin_user(actor=actor, target_user=target_user):
        raise PermissionDenied(
            "Пользователь не найден или недоступен для текущего администратора."
        )

    if actor and target_user and actor.id == target_user.id:
        raise ValidationError(
            {
                "user": (
                    "Администратор не может изменять собственные роли "
                    "через массовое или административное управление."
                )
            }
        )


def actor_has_organization_scope(
    *,
    actor,
    organization_id: int | None = None,
) -> bool:
    """
    Проверяет, есть ли у администратора доступ к организации.

    Args:
        actor:
            Администратор.
        organization_id:
            ID организации.

    Returns:
        bool: True, если организация доступна.
    """

    if not organization_id:
        return False

    return (
        get_actor_admin_roles_queryset(actor=actor)
        .filter(
            status=UserRoleStatus.ACTIVE,
            organization_id=organization_id,
            role__code__in=ORGANIZATION_ADMIN_ROLE_CODES,
        )
        .exists()
    )


def actor_has_department_scope(
    *,
    actor,
    department_id: int | None = None,
) -> bool:
    """
    Проверяет, есть ли у администратора доступ к отделению.

    Args:
        actor:
            Администратор.
        department_id:
            ID отделения.

    Returns:
        bool: True, если отделение доступно.
    """

    if not department_id:
        return False

    return (
        get_actor_admin_roles_queryset(actor=actor)
        .filter(
            status=UserRoleStatus.ACTIVE,
            department_id=department_id,
            role__code=RoleCode.DEPARTMENT_HEAD,
        )
        .exists()
    )


def validate_actor_can_assign_role(
    *,
    actor,
    role: Role,
    payload: AdminRoleAssignmentPayload,
) -> None:
    """
    Проверяет, может ли администратор назначить роль в указанном контексте.

    Args:
        actor:
            Администратор.
        role:
            Назначаемая роль.
        payload:
            Контекст назначения роли.

    Raises:
        PermissionDenied: Если назначение запрещено.
        ValidationError: Если контекст роли некорректен.
    """

    if is_superadmin(actor):
        return

    if (
        role.code in PROTECTED_ADMIN_ROLE_CODES
        or role.code in PLATFORM_ADMIN_ROLE_CODES
    ):
        raise PermissionDenied(
            "Только суперадминистратор может назначать административные роли платформы."
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
        if actor_has_department_scope(
            actor=actor,
            department_id=payload.department_id,
        ):
            return

    if actor_has_organization_scope(
        actor=actor,
        organization_id=payload.organization_id,
    ):
        return

    raise PermissionDenied(
        "У администратора нет прав назначать роль в указанном контексте."
    )


def validate_actor_can_revoke_user_role(
    *,
    actor,
    user_role: UserRole,
) -> None:
    """
    Проверяет, может ли администратор отозвать назначенную роль.

    Args:
        actor:
            Администратор.
        user_role:
            Назначенная роль пользователя.

    Raises:
        PermissionDenied: Если отзыв роли запрещён.
    """

    if is_superadmin(actor):
        return

    role_code = user_role.role.code

    if (
        role_code in PROTECTED_ADMIN_ROLE_CODES
        or role_code in PLATFORM_ADMIN_ROLE_CODES
    ):
        raise PermissionDenied(
            "Только суперадминистратор может отзывать административные роли платформы."
        )

    if user_role.department_id:
        if actor_has_department_scope(
            actor=actor,
            department_id=user_role.department_id,
        ):
            return

    if user_role.organization_id:
        if actor_has_organization_scope(
            actor=actor,
            organization_id=user_role.organization_id,
        ):
            return

    raise PermissionDenied(
        "У администратора нет прав отзывать роль в указанном контексте."
    )


def get_existing_user_role_for_assignment(
    *,
    target_user: User,
    role: Role,
    payload: AdminRoleAssignmentPayload,
) -> UserRole | None:
    """
    Ищет существующее назначение роли пользователя в том же контексте.

    Args:
        target_user:
            Пользователь.
        role:
            Роль.
        payload:
            Контекст назначения.

    Returns:
        UserRole | None: Найденное назначение роли или None.
    """

    return UserRole.objects.filter(
        user=target_user,
        role=role,
        organization_id=payload.organization_id,
        department_id=payload.department_id,
        group_id=payload.group_id,
    ).first()


def create_or_restore_user_role(
    *,
    actor,
    target_user: User,
    role: Role,
    payload: AdminRoleAssignmentPayload,
    reason: str = "",
) -> UserRole:
    """
    Создаёт или повторно активирует роль пользователя.

    Если такая роль уже была отозвана, отклонена или архивирована,
    она не создаётся повторно, а переводится в ACTIVE.

    Args:
        actor:
            Администратор.
        target_user:
            Пользователь.
        role:
            Роль.
        payload:
            Контекст назначения.
        reason:
            Причина назначения.

    Returns:
        UserRole: Назначенная роль.

    Raises:
        ValidationError: Если активная роль уже существует.
    """

    existing_user_role = get_existing_user_role_for_assignment(
        target_user=target_user,
        role=role,
        payload=payload,
    )

    if existing_user_role:
        if existing_user_role.status == UserRoleStatus.ACTIVE:
            raise ValidationError(
                {
                    "role": "У пользователя уже есть такая активная роль.",
                }
            )

        existing_user_role.status = UserRoleStatus.ACTIVE
        existing_user_role.assigned_by = actor
        existing_user_role.assigned_at = timezone.now()
        existing_user_role.revoked_by = None
        existing_user_role.revoked_at = None
        existing_user_role.revoke_reason = ""
        existing_user_role.save(
            update_fields=[
                "status",
                "assigned_by",
                "assigned_at",
                "revoked_by",
                "revoked_at",
                "revoke_reason",
                "updated_at",
            ]
        )

        return existing_user_role

    try:
        return UserRole.objects.create(
            user=target_user,
            role=role,
            organization_id=payload.organization_id,
            department_id=payload.department_id,
            group_id=payload.group_id,
            status=UserRoleStatus.ACTIVE,
            assigned_by=actor,
            assigned_at=timezone.now(),
        )
    except IntegrityError as error:
        raise ValidationError(
            {
                "role": (
                    "Не удалось назначить роль. Возможно, такая роль уже "
                    "существует в этом контексте."
                )
            }
        ) from error


def revoke_user_role_by_id(
    *,
    actor,
    target_user: User,
    user_role_id: int,
    reason: str = "",
) -> UserRole:
    """
    Отзывает назначенную роль пользователя по ID.

    Args:
        actor:
            Администратор.
        target_user:
            Пользователь.
        user_role_id:
            ID назначенной роли пользователя.
        reason:
            Причина отзыва.

    Returns:
        UserRole: Отозванная роль.

    Raises:
        ValidationError: Если назначение роли не найдено или уже отозвано.
    """

    user_role = (
        UserRole.objects.select_related(
            "role",
            "organization",
            "department",
            "group",
        )
        .filter(
            id=user_role_id,
            user=target_user,
        )
        .first()
    )

    if user_role is None:
        raise ValidationError(
            {
                "revoked_user_role_ids": "Назначенная роль пользователя не найдена.",
            }
        )

    if user_role.status == UserRoleStatus.REVOKED:
        raise ValidationError(
            {
                "revoked_user_role_ids": "Роль пользователя уже отозвана.",
            }
        )

    validate_actor_can_revoke_user_role(
        actor=actor,
        user_role=user_role,
    )

    user_role.revoke(
        user=actor,
        reason=reason,
        save=True,
    )

    return user_role


@transaction.atomic
def admin_change_user_roles(
    *,
    actor,
    target_user: User,
    assigned_roles: list[dict] | None = None,
    revoked_user_role_ids: list[int] | None = None,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
) -> dict:
    """
    Изменяет роли пользователя из административного раздела.

    Args:
        actor:
            Администратор, который меняет роли.
        target_user:
            Пользователь, которому меняют роли.
        assigned_roles:
            Список назначаемых ролей.
            Формат элемента:
                {
                    "role_id": 1,
                    "organization_id": 1,
                    "department_id": 2,
                    "group_id": 3
                }
        revoked_user_role_ids:
            Список ID назначенных ролей пользователя, которые нужно отозвать.
        reason:
            Причина изменения ролей.
        bulk_action_id:
            ID массового действия.
        request:
            HTTP-запрос.

    Returns:
        dict: Результат изменения ролей.

    Raises:
        PermissionDenied: Если нет прав.
        ValidationError: Если данные некорректны.
    """

    assigned_roles = assigned_roles or []
    revoked_user_role_ids = revoked_user_role_ids or []

    if not assigned_roles and not revoked_user_role_ids:
        raise ValidationError(
            {
                "roles": "Нужно передать роли для назначения или отзыва.",
            }
        )

    validate_actor_can_manage_target_roles(
        actor=actor,
        target_user=target_user,
    )
    validate_target_user_can_receive_roles(target_user=target_user)

    created_or_restored_user_roles = []
    revoked_user_roles = []

    for raw_payload in assigned_roles:
        payload = normalize_role_assignment_payload(raw_payload)
        role = get_role_for_assignment(role_id=payload.role_id)

        validate_actor_can_assign_role(
            actor=actor,
            role=role,
            payload=payload,
        )

        user_role = create_or_restore_user_role(
            actor=actor,
            target_user=target_user,
            role=role,
            payload=payload,
            reason=reason,
        )
        created_or_restored_user_roles.append(user_role)

    for user_role_id in revoked_user_role_ids:
        revoked_user_role = revoke_user_role_by_id(
            actor=actor,
            target_user=target_user,
            user_role_id=user_role_id,
            reason=reason,
        )
        revoked_user_roles.append(revoked_user_role)

    log_admin_user_roles_changed(
        actor=actor,
        target_user=target_user,
        assigned_role_ids=[
            user_role.role_id for user_role in created_or_restored_user_roles
        ],
        revoked_user_role_ids=[user_role.id for user_role in revoked_user_roles],
        reason=reason,
        bulk_action_id=bulk_action_id,
        request=request,
    )

    return {
        "assigned_user_role_ids": [
            user_role.id for user_role in created_or_restored_user_roles
        ],
        "revoked_user_role_ids": [user_role.id for user_role in revoked_user_roles],
    }
