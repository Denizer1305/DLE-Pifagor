from __future__ import annotations

from apps.users.permissions.helpers import (
    get_object_user,
    is_authenticated_active_user,
    is_organization_admin,
    is_safe_method,
    is_self,
    is_superadmin,
)
from rest_framework.permissions import BasePermission


class CanViewProfile(BasePermission):
    """
    Разрешает просмотр базового профиля пользователя.
    """

    message = "У вас нет прав на просмотр этого профиля."

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
        Проверяет объектный доступ к базовому профилю.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                Profile.

        Returns:
            bool: True, если доступ разрешён.
        """

        object_user = get_object_user(obj)

        if is_self(request.user, object_user):
            return True

        if is_superadmin(request.user):
            return True

        if is_safe_method(request):
            return True

        return False


class CanUpdateOwnProfile(BasePermission):
    """
    Разрешает пользователю изменять свой базовый профиль.
    """

    message = "Вы можете изменять только свой профиль."

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
        Проверяет право изменения базового профиля.

        Args:
            request:
                DRF request.
            view:
                DRF view.
            obj:
                Profile.

        Returns:
            bool: True, если профиль принадлежит пользователю.
        """

        object_user = get_object_user(obj)

        return is_self(request.user, object_user)


class CanModerateProfile(BasePermission):
    """
    Разрешает модерацию публичных данных профиля.
    """

    message = "У вас нет прав на модерацию профиля."

    def has_permission(self, request, view) -> bool:
        """
        Проверяет право модерации профилей.

        Args:
            request:
                DRF request.
            view:
                DRF view.

        Returns:
            bool: True, если пользователь суперадмин или администратор организации.
        """

        return is_superadmin(request.user) or is_organization_admin(request.user)
