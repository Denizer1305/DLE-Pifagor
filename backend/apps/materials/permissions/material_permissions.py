from __future__ import annotations

from apps.materials.permissions.shared import (
    user_can_manage_material_object,
    user_can_manage_materials_in_scope,
    user_can_read_material_object,
    user_can_read_materials,
)
from rest_framework.permissions import SAFE_METHODS, BasePermission


class MaterialPermission(BasePermission):
    """
    Ограничения доступа к учебным материалам.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию материалов.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_materials(request.user)

        return user_can_manage_materials_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному материалу.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_material_object(
                user=request.user,
                material=obj,
            )

        return user_can_manage_material_object(
            user=request.user,
            material=obj,
        )


class MaterialStatusPermission(BasePermission):
    """
    Ограничения для status-action материалов.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет базовое право на изменение статуса.
        """

        return user_can_manage_materials_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет право изменить статус конкретного материала.
        """

        return user_can_manage_material_object(
            user=request.user,
            material=obj,
        )
