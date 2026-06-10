from __future__ import annotations

from apps.education.permissions.shared import (
    EducationScopedPermission,
    get_payload_organization_ids_for_curriculum_item,
    user_can_access_object_by_organization,
    user_can_manage_object_by_organization,
    user_can_manage_scoped_education,
)
from rest_framework.permissions import SAFE_METHODS


class CurriculumItemPermission(EducationScopedPermission):
    """
    Ограничения доступа к элементам учебного плана.
    """

    payload_organization_getter = staticmethod(
        get_payload_organization_ids_for_curriculum_item,
    )

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет объектный доступ к элементу учебного плана.
        """

        if request.method in SAFE_METHODS:
            return user_can_access_object_by_organization(
                user=request.user,
                obj=obj,
            )

        return user_can_manage_scoped_education(
            request.user
        ) and user_can_manage_object_by_organization(
            user=request.user,
            obj=obj,
        )
