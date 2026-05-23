"""
Административная панель приложения users.

Подключает:
    - пользователей;
    - роли;
    - базовые профили;
    - профили учащихся;
    - профили родителей;
    - профили преподавателей;
    - связи родителей и учащихся;
    - коды приглашения;
    - заявки;
    - аудит.
"""

from apps.users.admin.audit_admin import RegistrationAttemptLogAdmin, UserAuditLogAdmin
from apps.users.admin.guardian_admin_profile import (
    GuardianLearnerAdmin,
    GuardianProfileAdmin,
)
from apps.users.admin.invite_code_admin import InviteCodeAdmin
from apps.users.admin.learner_admin_profile import LearnerProfileAdmin
from apps.users.admin.profile_admin import ProfileAdmin
from apps.users.admin.role_admin import RoleAdmin, UserRoleAdmin
from apps.users.admin.teacher_admin_profile import TeacherProfileAdmin
from apps.users.admin.user_admin import UserAdmin
from apps.users.admin.user_join_request_admin import UserJoinRequestAdmin

__all__ = [
    "GuardianLearnerAdmin",
    "GuardianProfileAdmin",
    "InviteCodeAdmin",
    "LearnerProfileAdmin",
    "ProfileAdmin",
    "RegistrationAttemptLogAdmin",
    "RoleAdmin",
    "TeacherProfileAdmin",
    "UserAdmin",
    "UserAuditLogAdmin",
    "UserJoinRequestAdmin",
    "UserRoleAdmin",
]
