from __future__ import annotations

from apps.users.permissions.helpers import (
    get_object_context,
    is_authenticated_active_user,
    is_organization_admin,
    is_safe_method,
    is_superadmin,
)
from rest_framework.permissions import BasePermission


class CanViewRoles(BasePermission):
    """
    Разрешает просмотр ролей активным пользователям.
    """

    message = "У вас нет прав на просмотр ролей."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет право просмотра ролей.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если пользователь активен.
        """

        return is_authenticated_active_user(request.user)


class CanManageSystemRoles(BasePermission):
    """
    Разрешает управление системными ролями только суперадминистратору.
    """

    message = "Управлять системными ролями может только суперадминистратор."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет право управления системными ролями.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если пользователь суперадминистратор.
        """

        return is_superadmin(request.user)


class CanAssignUserRole(BasePermission):
    """
    Разрешает назначение роли пользователю.

    Право имеют:
        - суперадминистратор;
        - администратор организации в своём контексте.

    Финальная проверка допустимости роли должна быть в service.
    """

    message = "У вас нет прав на назначение роли."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет общий доступ к назначению ролей.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если пользователь потенциально может назначать роли.
        """

        return is_superadmin(request.user) or is_organization_admin(request.user)


class CanRevokeUserRole(BasePermission):
    """
    Разрешает отзыв роли пользователя.
    """

    message = "У вас нет прав на отзыв роли."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет общий доступ.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если пользователь активен.
        """

        return is_authenticated_active_user(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право отзыва конкретной роли.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                UserRole.

        Returns:
            bool: True, если пользователь может отозвать роль.
        """

        if is_superadmin(request.user):
            return True

        context = get_object_context(obj)

        return is_organization_admin(
            request.user,
            organization=context["organization"],
            department=context["department"],
        )


class CanViewUserRole(BasePermission):
    """
    Разрешает просмотр назначенной роли пользователя.
    """

    message = "У вас нет прав на просмотр этой роли пользователя."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет общий доступ.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если пользователь активен.
        """

        return is_authenticated_active_user(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право просмотра роли пользователя.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                UserRole.

        Returns:
            bool: True, если доступ разрешён.
        """

        if obj.user_id == request.user.id:
            return True

        if is_superadmin(request.user):
            return True

        if is_safe_method(request):
            context = get_object_context(obj)

            return is_organization_admin(
                request.user,
                organization=context["organization"],
                department=context["department"],
            )

        return False
