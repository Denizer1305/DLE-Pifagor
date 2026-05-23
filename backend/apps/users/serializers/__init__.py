"""
Сериализаторы приложения users.

Сериализаторы отвечают за:
    - входные данные API;
    - выходное представление моделей;
    - простую валидацию формата.

Сложная бизнес-логика остаётся в users/services/.
"""

from apps.users.serializers.audit_serializers import (
    RegistrationAttemptLogSerializer,
    UserAuditLogSerializer,
)
from apps.users.serializers.auth_serializers import (
    AccessTokenSerializer,
    EmailVerificationSerializer,
    ForgotPasswordSerializer,
    LoginSerializer,
    RefreshTokenSerializer,
    ResendEmailVerificationSerializer,
    ResetPasswordSerializer,
    TokenPairSerializer,
)
from apps.users.serializers.current_profile_serializers import (
    CurrentProfileAvatarSerializer,
    CurrentProfileSerializer,
    CurrentProfileUpdateSerializer,
)
from apps.users.serializers.guardian_profile_serializers import (
    GuardianLearnerCreateSerializer,
    GuardianLearnerSerializer,
    GuardianProfileSerializer,
    GuardianProfileUpdateSerializer,
)
from apps.users.serializers.invite_code_serializers import (
    InviteCodeCreatedSerializer,
    InviteCodeCreateSerializer,
    InviteCodeSerializer,
)
from apps.users.serializers.learner_profile_serializers import (
    LearnerProfileSerializer,
    LearnerProfileUpdateSerializer,
    SubmitLearnerGroupRequestSerializer,
)
from apps.users.serializers.profile_serializers import (
    AvatarModerationSerializer,
    ProfileSerializer,
    ProfileUpdateSerializer,
)
from apps.users.serializers.registration_serializers import (
    BaseRegistrationSerializer,
    GuardianRegistrationSerializer,
    LearnerRegistrationSerializer,
    MinorLearnerRegistrationSerializer,
    TeacherRegistrationSerializer,
)
from apps.users.serializers.role_serializers import (
    RoleSerializer,
    RoleShortSerializer,
    UserRoleCreateSerializer,
    UserRoleSerializer,
)
from apps.users.serializers.teacher_profile_serializers import (
    PublicTeacherProfileSerializer,
    TeacherProfileSerializer,
    TeacherProfileUpdateSerializer,
)
from apps.users.serializers.user_join_request_serializers import (
    JoinRequestReviewSerializer,
    UserJoinRequestSerializer,
)
from apps.users.serializers.user_serializers import (
    UserDetailSerializer,
    UserShortSerializer,
    UserUpdateSerializer,
)
from apps.users.serializers.user_settings_serializers import (
    SetActiveRoleSerializer,
    UserSettingsSerializer,
    UserSettingsUpdateSerializer,
)

__all__ = [
    "AvatarModerationSerializer",
    "AccessTokenSerializer",
    "BaseRegistrationSerializer",
    "EmailVerificationSerializer",
    "GuardianLearnerCreateSerializer",
    "GuardianLearnerSerializer",
    "GuardianProfileSerializer",
    "GuardianProfileUpdateSerializer",
    "GuardianRegistrationSerializer",
    "InviteCodeCreatedSerializer",
    "InviteCodeCreateSerializer",
    "InviteCodeSerializer",
    "JoinRequestReviewSerializer",
    "LearnerProfileSerializer",
    "LearnerProfileUpdateSerializer",
    "LearnerRegistrationSerializer",
    "LoginSerializer",
    "MinorLearnerRegistrationSerializer",
    "ProfileSerializer",
    "ProfileUpdateSerializer",
    "PublicTeacherProfileSerializer",
    "RefreshTokenSerializer",
    "RegistrationAttemptLogSerializer",
    "ResendEmailVerificationSerializer",
    "RoleSerializer",
    "RoleShortSerializer",
    "SetActiveRoleSerializer",
    "SubmitLearnerGroupRequestSerializer",
    "TeacherProfileSerializer",
    "TeacherProfileUpdateSerializer",
    "TeacherRegistrationSerializer",
    "TokenPairSerializer",
    "UserAuditLogSerializer",
    "UserDetailSerializer",
    "UserJoinRequestSerializer",
    "UserRoleCreateSerializer",
    "UserRoleSerializer",
    "UserSettingsSerializer",
    "UserSettingsUpdateSerializer",
    "UserShortSerializer",
    "UserUpdateSerializer",
    "ForgotPasswordSerializer",
    "ResetPasswordSerializer",
    "CurrentProfileAvatarSerializer",
    "CurrentProfileSerializer",
    "CurrentProfileUpdateSerializer",
]
