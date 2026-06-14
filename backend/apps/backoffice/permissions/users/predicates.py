from __future__ import annotations

from apps.core.permissions import (
    is_active_user,
    is_organization_admin_role,
    is_superadmin,
)


def is_backoffice_user_actor(user) -> bool:
    """
    Проверяет, может ли пользователь войти в backoffice users.

    Доступ имеют:
    - superadmin / platform admin;
    - директор;
    - администратор организации;
    - заведующий отделением.

    Точная область видимости пользователей будет ограничиваться selectors.
    """

    if not is_active_user(user):
        return False

    return is_superadmin(user) or is_organization_admin_role(user)


def actor_can_access_backoffice_user(*, actor, target_user) -> bool:
    """
    Проверяет доступ администратора к конкретному пользователю.

    Импорт selector выполняется внутри функции, чтобы permissions
    не создавали циклический импорт при загрузке приложения.
    """

    if not is_backoffice_user_actor(actor):
        return False

    from apps.backoffice.selectors.users import (
        actor_can_access_backoffice_user as selector_actor_can_access_user,
    )

    return selector_actor_can_access_user(
        actor=actor,
        target_user=target_user,
    )


def actor_can_manage_backoffice_user(*, actor, target_user) -> bool:
    """
    Проверяет, может ли администратор управлять конкретным пользователем.

    На уровне permissions это тот же scope-доступ.
    Детальные бизнес-ограничения остаются в services.
    """

    return actor_can_access_backoffice_user(
        actor=actor,
        target_user=target_user,
    )
