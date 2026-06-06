from __future__ import annotations

from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.constants.roles import RoleCode
from apps.users.models import UserRole
from django.db.models import QuerySet


ORGANIZATION_ADMIN_ROLE_CODES = {
    RoleCode.ORG_ADMIN,
    RoleCode.DIRECTOR,
}

DEPARTMENT_ADMIN_ROLE_CODES = {
    RoleCode.DEPARTMENT_HEAD,
}

CURATOR_ROLE_CODES = {
    RoleCode.CURATOR,
}


def is_authenticated_active_actor(*, actor) -> bool:
    """
    Проверяет, что пользователь авторизован и активен.

    Args:
        actor:
            Пользователь, который выполняет действие.

    Returns:
        bool: True, если пользователь авторизован и активен.
    """

    return bool(
        actor
        and actor.is_authenticated
        and actor.is_active
    )


def is_superadmin_actor(*, actor) -> bool:
    """
    Проверяет, является ли пользователь суперадминистратором.

    Args:
        actor:
            Пользователь, который выполняет действие.

    Returns:
        bool: True, если пользователь является суперадминистратором.
    """

    return bool(
        is_authenticated_active_actor(actor=actor)
        and actor.is_superuser
    )


def get_actor_active_roles_queryset(*, actor) -> QuerySet:
    """
    Возвращает активные роли пользователя.

    Args:
        actor:
            Пользователь, который выполняет действие.

    Returns:
        QuerySet: Активные роли пользователя.
    """

    if not is_authenticated_active_actor(actor=actor):
        return UserRole.objects.none()

    return UserRole.objects.select_related(
        "role",
        "organization",
        "department",
        "group",
    ).filter(
        user=actor,
        status=UserRoleStatus.ACTIVE,
    )


def get_actor_organization_ids(*, actor) -> list[int]:
    """
    Возвращает ID организаций, доступных пользователю по активным ролям.

    Args:
        actor:
            Пользователь, который выполняет действие.

    Returns:
        list[int]: ID организаций.
    """

    return list(
        get_actor_active_roles_queryset(actor=actor)
        .filter(organization_id__isnull=False)
        .values_list("organization_id", flat=True)
        .distinct()
    )


def get_actor_department_ids(*, actor) -> list[int]:
    """
    Возвращает ID отделений, доступных пользователю по активным ролям.

    Args:
        actor:
            Пользователь, который выполняет действие.

    Returns:
        list[int]: ID отделений.
    """

    return list(
        get_actor_active_roles_queryset(actor=actor)
        .filter(department_id__isnull=False)
        .values_list("department_id", flat=True)
        .distinct()
    )


def get_actor_group_ids(*, actor) -> list[int]:
    """
    Возвращает ID групп, доступных пользователю по активным ролям.

    Args:
        actor:
            Пользователь, который выполняет действие.

    Returns:
        list[int]: ID групп.
    """

    return list(
        get_actor_active_roles_queryset(actor=actor)
        .filter(group_id__isnull=False)
        .values_list("group_id", flat=True)
        .distinct()
    )


def get_actor_admin_organization_ids(*, actor) -> list[int]:
    """
    Возвращает ID организаций, где пользователь является администратором.

    Args:
        actor:
            Пользователь, который выполняет административное действие.

    Returns:
        list[int]: ID организаций.
    """

    return list(
        get_actor_active_roles_queryset(actor=actor)
        .filter(
            role__code__in=ORGANIZATION_ADMIN_ROLE_CODES,
            organization_id__isnull=False,
        )
        .values_list("organization_id", flat=True)
        .distinct()
    )


def get_actor_admin_department_ids(*, actor) -> list[int]:
    """
    Возвращает ID отделений, где пользователь является заведующим.

    Args:
        actor:
            Пользователь, который выполняет административное действие.

    Returns:
        list[int]: ID отделений.
    """

    return list(
        get_actor_active_roles_queryset(actor=actor)
        .filter(
            role__code__in=DEPARTMENT_ADMIN_ROLE_CODES,
            department_id__isnull=False,
        )
        .values_list("department_id", flat=True)
        .distinct()
    )


def actor_has_organization_admin_access(*, actor) -> bool:
    """
    Проверяет, есть ли у пользователя административный доступ к организации.

    Args:
        actor:
            Пользователь.

    Returns:
        bool: True, если доступ есть.
    """

    if is_superadmin_actor(actor=actor):
        return True

    return bool(get_actor_admin_organization_ids(actor=actor))


def actor_has_department_admin_access(*, actor) -> bool:
    """
    Проверяет, есть ли у пользователя административный доступ к отделению.

    Args:
        actor:
            Пользователь.

    Returns:
        bool: True, если доступ есть.
    """

    if is_superadmin_actor(actor=actor):
        return True

    return bool(get_actor_admin_department_ids(actor=actor))


def actor_can_access_organization_id(
    *,
    actor,
    organization_id: int | None,
) -> bool:
    """
    Проверяет доступ пользователя к организации.

    Args:
        actor:
            Пользователь.
        organization_id:
            ID организации.

    Returns:
        bool: True, если организация доступна.
    """

    if not organization_id:
        return False

    if is_superadmin_actor(actor=actor):
        return True

    return organization_id in get_actor_organization_ids(actor=actor)


def actor_can_admin_organization_id(
    *,
    actor,
    organization_id: int | None,
) -> bool:
    """
    Проверяет административный доступ пользователя к организации.

    Args:
        actor:
            Пользователь.
        organization_id:
            ID организации.

    Returns:
        bool: True, если административный доступ есть.
    """

    if not organization_id:
        return False

    if is_superadmin_actor(actor=actor):
        return True

    return organization_id in get_actor_admin_organization_ids(actor=actor)


def actor_can_admin_department_id(
    *,
    actor,
    department_id: int | None,
) -> bool:
    """
    Проверяет административный доступ пользователя к отделению.

    Args:
        actor:
            Пользователь.
        department_id:
            ID отделения.

    Returns:
        bool: True, если административный доступ есть.
    """

    if not department_id:
        return False

    if is_superadmin_actor(actor=actor):
        return True

    return department_id in get_actor_admin_department_ids(actor=actor)