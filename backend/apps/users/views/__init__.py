"""
Views приложения users.

Views принимают HTTP-запросы, вызывают serializers и services,
а затем возвращают HTTP-ответы.

Бизнес-логика должна оставаться в users/services/.
"""

from apps.users.views.auth_views import (
    ForgotPasswordView,
    GuardianRegistrationView,
    LearnerRegistrationView,
    LoginView,
    LogoutView,
    MinorLearnerRegistrationView,
    RefreshTokenView,
    ResetPasswordView,
    TeacherRegistrationView,
    VerifyEmailView,
)
from apps.users.views.guardian_profile_views import (
    GuardianLearnerViewSet,
    GuardianProfileViewSet,
)
from apps.users.views.invite_code_views import InviteCodeViewSet
from apps.users.views.learner_profile_views import LearnerProfileViewSet
from apps.users.views.profile_views import ProfileViewSet
from apps.users.views.role_views import RoleViewSet, UserRoleViewSet
from apps.users.views.teacher_profile_views import TeacherProfileViewSet
from apps.users.views.user_join_request_views import UserJoinRequestViewSet
from apps.users.views.user_settings_views import UserSettingsViewSet
from apps.users.views.user_views import UserViewSet

__all__ = [
    "GuardianLearnerViewSet",
    "GuardianProfileViewSet",
    "GuardianRegistrationView",
    "InviteCodeViewSet",
    "LearnerProfileViewSet",
    "LearnerRegistrationView",
    "LoginView",
    "LogoutView",
    "MinorLearnerRegistrationView",
    "ProfileViewSet",
    "RoleViewSet",
    "TeacherProfileViewSet",
    "TeacherRegistrationView",
    "UserJoinRequestViewSet",
    "UserRoleViewSet",
    "UserSettingsViewSet",
    "UserViewSet",
    "VerifyEmailView",
    "RefreshTokenView",
    "ForgotPasswordView",
    "ResetPasswordView",
]
