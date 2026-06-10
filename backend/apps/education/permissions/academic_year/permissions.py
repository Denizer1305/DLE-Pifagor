from __future__ import annotations

from apps.education.permissions.shared import EducationGlobalMutationPermission


class AcademicYearPermission(EducationGlobalMutationPermission):
    """
    Ограничения доступа к учебным годам.
    """
