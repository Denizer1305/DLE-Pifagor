from __future__ import annotations

from apps.materials.permissions.shared import (
    user_can_manage_material_version_object,
    user_can_manage_materials_in_scope,
    user_can_read_material_version_object,
    user_can_read_materials,
)
from rest_framework.permissions import SAFE_METHODS, BasePermission


class MaterialVersionPermission(BasePermission):
    """
    Ограничения доступа к версиям материалов.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию версий.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_materials(request.user)

        return user_can_manage_materials_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретной версии материала.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_material_version_object(
                user=request.user,
                version=obj,
            )

        return user_can_manage_material_version_object(
            user=request.user,
            version=obj,
        )


class MaterialVersionSetCurrentPermission(BasePermission):
    """
    Ограничение для действия назначения текущей версии.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет базовое право управления версиями.
        """

        return user_can_manage_materials_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право сделать конкретную версию текущей.
        """

        return user_can_manage_material_version_object(
            user=request.user,
            version=obj,
        )
