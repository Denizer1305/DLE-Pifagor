from apps.organizations.admin.department_admin import DepartmentAdmin
from apps.organizations.admin.group_curator_admin import GroupCuratorAdmin
from apps.organizations.admin.organization_admin import OrganizationAdmin
from apps.organizations.admin.study_group_admin import StudyGroupAdmin
from apps.organizations.admin.subject_admin import SubjectAdmin
from apps.organizations.admin.teacher_organization_admin import (
    TeacherOrganizationAdmin,
)
from apps.organizations.admin.teacher_subject_admin import TeacherSubjectAdmin

__all__ = [
    "DepartmentAdmin",
    "GroupCuratorAdmin",
    "OrganizationAdmin",
    "StudyGroupAdmin",
    "SubjectAdmin",
    "TeacherOrganizationAdmin",
    "TeacherSubjectAdmin",
]