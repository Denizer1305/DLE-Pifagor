from __future__ import annotations


def is_authenticated_user(*, user) -> bool:
    """
    Проверяет, что пользователь авторизован.
    """

    return bool(user and getattr(user, "is_authenticated", False))


def is_superadmin(*, user) -> bool:
    """
    Проверяет права суперпользователя.
    """

    return bool(
        is_authenticated_user(user=user) and getattr(user, "is_superuser", False)
    )


def user_has_role_code(
    *,
    user,
    role_code: str,
) -> bool:
    """
    Проверяет наличие активной роли у пользователя.

    Сделано устойчиво к текущей реализации users:
    - direct role;
    - user_roles.
    """

    if not is_authenticated_user(user=user):
        return False

    direct_role = getattr(user, "role", None)
    direct_role_code = getattr(direct_role, "code", None)

    if direct_role_code == role_code:
        return True

    user_roles = getattr(user, "user_roles", None)

    if user_roles is None:
        return False

    for user_role in user_roles.all():
        status = getattr(user_role, "status", "active")

        if status != "active":
            continue

        role = getattr(user_role, "role", None)

        if getattr(role, "code", None) == role_code:
            return True

    return False


def is_teacher(*, user) -> bool:
    """
    Проверяет роль преподавателя.
    """

    return user_has_role_code(user=user, role_code="teacher")


def is_learner(*, user) -> bool:
    """
    Проверяет роль обучающегося.
    """

    return user_has_role_code(user=user, role_code="learner")


def is_guardian(*, user) -> bool:
    """
    Проверяет роль родителя.
    """

    return user_has_role_code(user=user, role_code="guardian")


def is_testing_admin(*, user) -> bool:
    """
    Проверяет административный доступ к тестированию.
    """

    if is_superadmin(user=user):
        return True

    admin_roles = {
        "admin",
        "organization_admin",
        "director",
        "head_of_department",
    }

    return any(
        user_has_role_code(user=user, role_code=role_code) for role_code in admin_roles
    )
