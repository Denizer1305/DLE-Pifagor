from __future__ import annotations

from apps.users.permissions.helpers import is_authenticated_active_user, is_superadmin
from rest_framework.permissions import BasePermission


class IsActiveUser(BasePermission):
    """
    Разрешает доступ только активному авторизованному пользователю.
    """

    message = "Для доступа необходимо войти в активный аккаунт."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ на уровне запроса.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если пользователь активен и авторизован.
        """

        return is_authenticated_active_user(request.user)


class IsSuperAdminRole(BasePermission):
    """
    Разрешает доступ только суперадминистратору платформы.
    """

    message = "Доступ разрешён только суперадминистратору платформы."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет наличие роли superadmin.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если пользователь является суперадминистратором.
        """

        return is_superadmin(request.user)
