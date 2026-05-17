"""
Административная панель приложения organizations.

Подключает:
    - образовательные организации;
    - отделения;
    - учебные группы.
"""

from apps.organizations.admin.department_admin import DepartmentAdmin
from apps.organizations.admin.organization_admin import OrganizationAdmin
from apps.organizations.admin.study_group_admin import StudyGroupAdmin

__all__ = [
    "DepartmentAdmin",
    "OrganizationAdmin",
    "StudyGroupAdmin",
]
