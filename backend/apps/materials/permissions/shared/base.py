from __future__ import annotations

from apps.materials.permissions.shared.role_checks import (
    user_can_manage_materials_globally,
    user_can_manage_materials_in_scope,
    user_can_read_materials,
)
from rest_framework.permissions import SAFE_METHODS, BasePermission


class MaterialReadOnlyOrScopedWritePermission(BasePermission):
    """
    Базовое ограничение: читать могут авторизованные пользователи,
    изменять — пользователи с правом управления материалами.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ на уровне запроса.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_materials(request.user)

        return user_can_manage_materials_in_scope(request.user)


class MaterialGlobalAdminOnlyPermission(BasePermission):
    """
    Ограничение только для глобальных администраторов.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет глобальный административный доступ.
        """

        return user_can_manage_materials_globally(request.user)


class MaterialAuthenticatedReadPermission(BasePermission):
    """
    Ограничение только на авторизованное чтение.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет авторизацию пользователя.
        """

        return user_can_read_materials(request.user)
