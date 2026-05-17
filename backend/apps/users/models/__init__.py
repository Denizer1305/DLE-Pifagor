"""
Модели приложения users.

Приложение users отвечает за:
    - пользователей;
    - роли;
    - ролевые профили;
    - связи родитель–учащийся;
    - коды приглашения;
    - заявки;
    - настройки;
    - аудит.
"""

from apps.users.models.audit import RegistrationAttemptLog, UserAuditLog
from apps.users.models.guardian_learner import GuardianLearner
from apps.users.models.guardian_profile import GuardianProfile
from apps.users.models.invite_code import InviteCode
from apps.users.models.learner_profile import LearnerProfile
from apps.users.models.profile import Profile
from apps.users.models.role import Role, UserRole
from apps.users.models.teacher_profile import TeacherProfile
from apps.users.models.user import User
from apps.users.models.user_join_request import UserJoinRequest
from apps.users.models.user_settings import UserSettings

__all__ = [
    "GuardianLearner",
    "GuardianProfile",
    "InviteCode",
    "LearnerProfile",
    "Profile",
    "RegistrationAttemptLog",
    "Role",
    "TeacherProfile",
    "User",
    "UserAuditLog",
    "UserJoinRequest",
    "UserRole",
    "UserSettings",
]
