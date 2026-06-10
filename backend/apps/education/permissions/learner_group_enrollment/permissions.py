from __future__ import annotations

from apps.education.permissions.shared import (
    EducationScopedPermission,
    get_payload_organization_ids_for_learner_group_enrollment,
    user_can_access_learner_enrollment,
    user_can_access_object_by_group,
    user_can_access_object_by_organization,
    user_can_manage_object_by_group,
    user_can_manage_scoped_education,
)
from rest_framework.permissions import SAFE_METHODS


class LearnerGroupEnrollmentPermission(EducationScopedPermission):
    """
    Ограничения доступа к академическим зачислениям обучающихся.
    """

    payload_organization_getter = staticmethod(
        get_payload_organization_ids_for_learner_group_enrollment,
    )

    def has_object_permission(self, request, view, obj) -> bool:
        """
        Проверяет объектный доступ к академическому зачислению.
        """

        if request.method in SAFE_METHODS:
            return (
                user_can_access_learner_enrollment(user=request.user, obj=obj)
                or user_can_access_object_by_group(user=request.user, obj=obj)
                or user_can_access_object_by_organization(user=request.user, obj=obj)
            )

        return user_can_manage_scoped_education(
            request.user
        ) and user_can_manage_object_by_group(user=request.user, obj=obj)
