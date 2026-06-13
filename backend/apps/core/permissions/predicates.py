from __future__ import annotations

from collections.abc import Iterable

from rest_framework.permissions import SAFE_METHODS


def is_authenticated_user(user) -> bool:
    """
    Проверяет, что пользователь авторизован.
    """

    return bool(user and user.is_authenticated)


def is_active_user(user) -> bool:
    """
    Проверяет, что пользователь авторизован и активен.
    """

    return bool(
        is_authenticated_user(user)
        and getattr(user, "is_active", False)
    )


def is_authenticated_active_user(user) -> bool:
    """
    Алиас для обратной совместимости с существующими permissions.
    """

    return is_active_user(user)


def is_safe_method(request) -> bool:
    """
    Проверяет, что HTTP-метод является безопасным.
    """

    return request.method in SAFE_METHODS


def has_role(
    *,
    user,
    role_code: str,
    organization=None,
    department=None,
    group=None,
) -> bool:
    """
    Проверяет наличие активной роли у пользователя.

    Импорт role selector выполняется внутри функции, чтобы core не создавал
    циклический импорт при загрузке users.
    """

    if not is_active_user(user):
        return False

    from apps.users.selectors.role_selectors import user_has_active_role

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
    """

    if not is_active_user(user):
        return False

    if getattr(user, "is_superuser", False):
        return True

    from apps.users.constants.roles import PLATFORM_ADMIN_ROLE_CODES

    return has_any_role(
        user=user,
        role_codes=PLATFORM_ADMIN_ROLE_CODES,
    )


def is_teacher(user, *, organization=None, department=None, group=None) -> bool:
    """
    Проверяет роль преподавателя.
    """

    from apps.users.constants.roles import RoleCode

    return has_role(
        user=user,
        role_code=RoleCode.TEACHER,
        organization=organization,
        department=department,
        group=group,
    )


def is_learner(user, *, organization=None, department=None, group=None) -> bool:
    """
    Проверяет роль учащегося.
    """

    from apps.users.constants.roles import RoleCode

    return has_role(
        user=user,
        role_code=RoleCode.LEARNER,
        organization=organization,
        department=department,
        group=group,
    )


def is_guardian(user, *, organization=None, department=None, group=None) -> bool:
    """
    Проверяет роль родителя или законного представителя.
    """

    from apps.users.constants.roles import RoleCode

    return has_role(
        user=user,
        role_code=RoleCode.GUARDIAN,
        organization=organization,
        department=department,
        group=group,
    )


def is_staff_user(user, *, organization=None, department=None, group=None) -> bool:
    """
    Проверяет, относится ли пользователь к сотрудникам организации.
    """

    from apps.users.constants.roles import STAFF_ROLE_CODES

    return has_any_role(
        user=user,
        role_codes=STAFF_ROLE_CODES,
        organization=organization,
        department=department,
        group=group,
    )


def is_platform_admin(user) -> bool:
    """
    Проверяет платформенную административную роль.
    """

    from apps.users.constants.roles import PLATFORM_ADMIN_ROLE_CODES

    return has_any_role(
        user=user,
        role_codes=PLATFORM_ADMIN_ROLE_CODES,
    )


def is_organization_admin_role(
    user,
    *,
    organization=None,
    department=None,
    group=None,
) -> bool:
    """
    Проверяет административную роль внутри организации.

    Это только role-predicate. Доменные правила доступа к объектам
    должны оставаться внутри конкретного приложения.
    """

    from apps.users.constants.roles import ORGANIZATION_ADMIN_ROLE_CODES

    return has_any_role(
        user=user,
        role_codes=ORGANIZATION_ADMIN_ROLE_CODES,
        organization=organization,
        department=department,
        group=group,
    )