from __future__ import annotations

from apps.backoffice.permissions.users.predicates import (
    actor_can_access_backoffice_user,
    actor_can_manage_backoffice_user,
    is_backoffice_user_actor,
)
from rest_framework.permissions import BasePermission


class CanAccessBackofficeUsers(BasePermission):
    """
    Разрешает доступ к административному разделу пользователей.

    Permission проверяет:
    - общий доступ к backoffice users;
    - объектный доступ к конкретному пользователю.

    Список доступных пользователей должен ограничиваться selector'ом.
    """

    message = "У вас нет прав на доступ к административному управлению пользователями."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет общий доступ к административному разделу пользователей.
        """

        return is_backoffice_user_actor(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному пользователю.
        """

        return actor_can_access_backoffice_user(
            actor=request.user,
            target_user=obj,
        )


class CanManageBackofficeUser(CanAccessBackofficeUsers):
    """
    Разрешает административное редактирование пользователя.

    Детальные правила изменения полей проверяются в service-слое.
    """

    message = "У вас нет прав на изменение этого пользователя."

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет объектный доступ к управлению пользователем.
        """

        return actor_can_manage_backoffice_user(
            actor=request.user,
            target_user=obj,
        )


class CanCreateBackofficeUser(CanAccessBackofficeUsers):
    """
    Разрешает административное создание пользователя.

    Конкретные ограничения по организации, ролям и профилям
    должны проверяться в service-слое создания пользователя.
    """

    message = "У вас нет прав на создание пользователя."


class CanDeleteBackofficeUser(CanManageBackofficeUser):
    """
    Разрешает административное удаление или планирование удаления пользователя.

    Запрет удаления самого себя проверяется в service-слое.
    """

    message = "У вас нет прав на удаление этого пользователя."


class CanManageBackofficeUserStatus(CanManageBackofficeUser):
    """
    Разрешает административное управление статусом пользователя.

    Используется для:
    - блокировки;
    - разблокировки;
    - архивации;
    - восстановления.
    """

    message = "У вас нет прав на изменение статуса этого пользователя."


class CanManageBackofficeUserRoles(CanManageBackofficeUser):
    """
    Разрешает административное управление ролями пользователя.

    Permission проверяет только доступ к пользователю.
    Возможность назначить или отозвать конкретную роль проверяет service-слой.
    """

    message = "У вас нет прав на изменение ролей этого пользователя."


class CanBulkManageBackofficeUsers(CanAccessBackofficeUsers):
    """
    Разрешает массовые административные действия над пользователями.

    Permission даёт доступ только к endpoint'у.
    Проверка каждого пользователя из списка выполняется в bulk services.
    """

    message = "У вас нет прав на массовое управление пользователями."


class CanViewBackofficeUserAudit(CanAccessBackofficeUsers):
    """
    Разрешает просмотр audit-лога пользователя.

    Объектный доступ проверяется по самому пользователю,
    а не по audit-записи.
    """

    message = "У вас нет прав на просмотр истории действий по этому пользователю."
