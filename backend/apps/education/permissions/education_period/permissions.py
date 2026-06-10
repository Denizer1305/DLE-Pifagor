from __future__ import annotations

from apps.education.permissions.shared import EducationGlobalMutationPermission


class EducationPeriodPermission(EducationGlobalMutationPermission):
    """
    Ограничения доступа к учебным периодам.
    """
