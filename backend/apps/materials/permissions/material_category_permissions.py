from __future__ import annotations

from apps.materials.permissions.shared import (
    user_can_manage_material_category_object,
    user_can_manage_materials_in_scope,
    user_can_read_material_category_object,
    user_can_read_materials,
)
from rest_framework.permissions import SAFE_METHODS, BasePermission


class MaterialCategoryPermission(BasePermission):
    """
    Ограничения доступа к категориям материалов.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к списку и созданию категорий.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_materials(request.user)

        return user_can_manage_materials_in_scope(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретной категории.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_material_category_object(
                user=request.user,
                category=obj,
            )

        return user_can_manage_material_category_object(
            user=request.user,
            category=obj,
        )
