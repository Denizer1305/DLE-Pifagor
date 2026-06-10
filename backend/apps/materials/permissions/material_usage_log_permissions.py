from __future__ import annotations

from apps.materials.permissions.shared import (
    user_can_manage_materials_globally,
    user_can_manage_usage_log_object,
    user_can_read_materials,
    user_can_read_usage_log_object,
)
from rest_framework.permissions import SAFE_METHODS, BasePermission


class MaterialUsageLogPermission(BasePermission):
    """
    Ограничения доступа к журналу использования материалов.
    """

    def has_permission(self, request, view) -> bool:
        """
        Проверяет доступ к журналу использования.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_materials(request.user)

        return user_can_manage_materials_globally(request.user)

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет доступ к конкретному событию журнала.
        """

        if request.method in SAFE_METHODS:
            return user_can_read_usage_log_object(
                user=request.user,
                usage_log=obj,
            )

        return user_can_manage_usage_log_object(
            user=request.user,
            usage_log=obj,
        )
