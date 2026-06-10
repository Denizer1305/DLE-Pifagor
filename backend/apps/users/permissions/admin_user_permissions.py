from __future__ import annotations

from apps.users.permissions.helpers import (
    is_authenticated_active_user,
    is_organization_admin,
    is_superadmin,
)
from apps.users.selectors.admin_user_selectors import actor_can_access_admin_user
from rest_framework.permissions import BasePermission


class CanAccessAdminUsers(BasePermission):
    """
    Разрешает доступ к административному разделу пользователей.

    Доступ имеют:
        - суперадминистратор;
        - директор;
        - администратор организации;
        - заведующий отделением.

    Точный список пользователей ограничивается selector'ом.
    """

    message = "У вас нет прав на доступ к административному управлению пользователями."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к административному разделу пользователей.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если доступ разрешён.
        """

        user = request.user

        return is_authenticated_active_user(user) and (
            is_superadmin(user) or is_organization_admin(user)
        )

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному пользователю.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                Целевой пользователь.

        Returns:
            bool: True, если доступ разрешён.
        """

        return actor_can_access_admin_user(
            actor=request.user,
            target_user=obj,
        )


class CanManageAdminUser(CanAccessAdminUsers):
    """
    Разрешает административное редактирование пользователя.

    Важно:
        Permission проверяет только общий доступ к пользователю.
        Детальные правила изменения email, ролей, статуса и lifecycle
        должны находиться в сервисном слое.
    """

    message = "У вас нет прав на изменение этого пользователя."


class CanManageAdminUserStatus(CanAccessAdminUsers):
    """
    Разрешает административное управление статусом пользователя.

    Используется для:
        - блокировки;
        - разблокировки;
        - архивации;
        - восстановления;
        - планирования удаления.
    """

    message = "У вас нет прав на изменение статуса этого пользователя."


class CanManageAdminUserRoles(CanAccessAdminUsers):
    """
    Разрешает административное управление ролями пользователя.

    Важно:
        Суперадминистратор сможет менять все роли.
        Ограничения администратора организации, директора и заведующего
        будут проверяться в role_services.py.
    """

    message = "У вас нет прав на изменение ролей этого пользователя."


class CanBulkManageAdminUsers(CanAccessAdminUsers):
    """
    Разрешает массовые административные действия над пользователями.

    Важно:
        Permission даёт доступ только к endpoint'у.
        Проверка каждого пользователя из списка выполняется в bulk_services.py.
    """

    message = "У вас нет прав на массовое управление пользователями."
