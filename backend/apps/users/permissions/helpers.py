from __future__ import annotations

from typing import Iterable

from apps.users.constants.roles import (
    GUARDIAN_REVIEWER_ROLE_CODES,
    LEARNER_REVIEWER_ROLE_CODES,
    ORGANIZATION_ADMIN_ROLE_CODES,
    ORGANIZATION_REVIEWER_ROLE_CODES,
    PLATFORM_ADMIN_ROLE_CODES,
    TEACHER_REVIEWER_ROLE_CODES,
    RoleCode,
)
from apps.users.selectors.role_selectors import user_has_active_role
from rest_framework.permissions import SAFE_METHODS


def is_authenticated_active_user(user) -> bool:
    """
    Проверяет, является ли пользователь авторизованным и активным.

    Args:
        user:
            Пользователь из request.user.

    Returns:
        bool: True, если пользователь авторизован и активен.
    """

    return bool(user and user.is_authenticated and getattr(user, "is_active", False))


def is_safe_method(request) -> bool:
    """
    Проверяет, является ли HTTP-метод безопасным.

    Args:
        request:
            DRF request.

    Returns:
        bool: True, если метод GET, HEAD или OPTIONS.
    """

    return request.method in SAFE_METHODS


def is_self(user, target_user) -> bool:
    """
    Проверяет, совпадает ли пользователь с целевым пользователем.

    Args:
        user:
            Текущий пользователь.
        target_user:
            Целевой пользователь.

    Returns:
        bool: True, если это один и тот же пользователь.
    """

    return bool(user and target_user and user == target_user)


def get_object_user(obj):
    """
    Извлекает пользователя из объекта.

    Args:
        obj:
            Объект проверки.

    Returns:
        User | None: Пользователь объекта или None.
    """

    if obj is None:
        return None

    if hasattr(obj, "user"):
        return obj.user

    if hasattr(obj, "target_user"):
        return obj.target_user

    return None


def get_object_context(obj) -> dict:
    """
    Извлекает организационный контекст объекта.

    Args:
        obj:
            Объект проверки.

    Returns:
        dict: organization, department и group.
    """

    if obj is None:
        return {
            "organization": None,
            "department": None,
            "group": None,
        }

    return {
        "organization": getattr(obj, "organization", None),
        "department": getattr(obj, "department", None),
        "group": getattr(obj, "group", None),
    }


def has_role(
    *,
    user,
    role_code: str,
    organization=None,
    department=None,
    group=None,
) -> bool:
    """
    Проверяет, есть ли у пользователя активная роль.

    Args:
        user:
            Пользователь.
        role_code:
            Код роли.
        organization:
            Организация.
        department:
            Отделение.
        group:
            Группа.

    Returns:
        bool: True, если роль найдена.
    """

    if not is_authenticated_active_user(user):
        return False

    return user_has_active_role(
        user=user,
        role_code=role_code,
        organization=organization,
        department=department,
        group=group,
    )


def has_any_role(
    *,
    user,
    role_codes: Iterable[str],
    organization=None,
    department=None,
    group=None,
) -> bool:
    """
    Проверяет, есть ли у пользователя хотя бы одна роль из списка.

    Args:
        user:
            Пользователь.
        role_codes:
            Коды ролей.
        organization:
            Организация.
        department:
            Отделение.
        group:
            Группа.

    Returns:
        bool: True, если найдена хотя бы одна роль.
    """

    return any(
        has_role(
            user=user,
            role_code=role_code,
            organization=organization,
            department=department,
            group=group,
        )
        for role_code in role_codes
    )


def is_superadmin(user) -> bool:
    """
    Проверяет, является ли пользователь суперадминистратором платформы.

    Args:
        user:
            Пользователь.

    Returns:
        bool: True, если у пользователя есть роль superadmin.
    """

    if not is_authenticated_active_user(user):
        return False

    if getattr(user, "is_superuser", False):
        return True

    return has_any_role(
        user=user,
        role_codes=PLATFORM_ADMIN_ROLE_CODES,
    )


def is_organization_admin(user, *, organization=None, department=None) -> bool:
    """
    Проверяет, может ли пользователь управлять организацией.

    Args:
        user:
            Пользователь.
        organization:
            Организация.
        department:
            Отделение.

    Returns:
        bool: True, если пользователь является администратором контекста.
    """

    if is_superadmin(user):
        return True

    if organization is None:
        return has_any_role(
            user=user,
            role_codes=ORGANIZATION_ADMIN_ROLE_CODES,
        )

    return (
        has_role(
            user=user,
            role_code=RoleCode.DIRECTOR,
            organization=organization,
        )
        or has_role(
            user=user,
            role_code=RoleCode.ORG_ADMIN,
            organization=organization,
        )
        or has_role(
            user=user,
            role_code=RoleCode.DEPARTMENT_HEAD,
            organization=organization,
            department=department,
        )
    )


def is_organization_reviewer(
    user, *, organization=None, department=None, group=None
) -> bool:
    """
    Проверяет, может ли пользователь рассматривать заявки организации.

    Args:
        user:
            Пользователь.
        organization:
            Организация.
        department:
            Отделение.
        group:
            Группа.

    Returns:
        bool: True, если пользователь может рассматривать заявки.
    """

    if is_superadmin(user):
        return True

    if organization is None:
        return has_any_role(
            user=user,
            role_codes=ORGANIZATION_REVIEWER_ROLE_CODES,
        )

    return (
        has_role(user=user, role_code=RoleCode.ORG_ADMIN, organization=organization)
        or has_role(user=user, role_code=RoleCode.DIRECTOR, organization=organization)
        or has_role(
            user=user,
            role_code=RoleCode.DEPARTMENT_HEAD,
            organization=organization,
            department=department,
        )
        or has_role(
            user=user,
            role_code=RoleCode.CURATOR,
            organization=organization,
            group=group,
        )
    )


def can_review_teacher(user, *, organization=None, department=None) -> bool:
    """
    Проверяет, может ли пользователь подтверждать преподавателя.

    Args:
        user:
            Пользователь.
        organization:
            Организация.
        department:
            Отделение.

    Returns:
        bool: True, если пользователь может подтверждать преподавателей.
    """

    if is_superadmin(user):
        return True

    if organization is None:
        return has_any_role(user=user, role_codes=TEACHER_REVIEWER_ROLE_CODES)

    return (
        has_role(user=user, role_code=RoleCode.DIRECTOR, organization=organization)
        or has_role(user=user, role_code=RoleCode.ORG_ADMIN, organization=organization)
        or has_role(
            user=user,
            role_code=RoleCode.DEPARTMENT_HEAD,
            organization=organization,
            department=department,
        )
    )


def can_review_learner(user, *, organization=None, department=None, group=None) -> bool:
    """
    Проверяет, может ли пользователь подтверждать учащегося.

    Args:
        user:
            Пользователь.
        organization:
            Организация.
        department:
            Отделение.
        group:
            Группа.

    Returns:
        bool: True, если пользователь может подтверждать учащихся.
    """

    if is_superadmin(user):
        return True

    if organization is None:
        return has_any_role(user=user, role_codes=LEARNER_REVIEWER_ROLE_CODES)

    return (
        has_role(user=user, role_code=RoleCode.ORG_ADMIN, organization=organization)
        or has_role(
            user=user,
            role_code=RoleCode.DEPARTMENT_HEAD,
            organization=organization,
            department=department,
        )
        or has_role(
            user=user,
            role_code=RoleCode.CURATOR,
            organization=organization,
            group=group,
        )
    )


def can_review_guardian_link(
    user, *, organization=None, department=None, group=None
) -> bool:
    """
    Проверяет, может ли пользователь подтверждать связь родителя и учащегося.

    Args:
        user:
            Пользователь.
        organization:
            Организация.
        department:
            Отделение.
        group:
            Группа.

    Returns:
        bool: True, если пользователь может подтверждать связь.
    """

    if is_superadmin(user):
        return True

    if organization is None:
        return has_any_role(user=user, role_codes=GUARDIAN_REVIEWER_ROLE_CODES)

    return (
        has_role(user=user, role_code=RoleCode.ORG_ADMIN, organization=organization)
        or has_role(
            user=user,
            role_code=RoleCode.DEPARTMENT_HEAD,
            organization=organization,
            department=department,
        )
        or has_role(
            user=user,
            role_code=RoleCode.CURATOR,
            organization=organization,
            group=group,
        )
    )
