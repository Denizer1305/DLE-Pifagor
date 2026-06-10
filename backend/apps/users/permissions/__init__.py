"""
Ограничения доступа приложения users.

Permissions отвечают только на вопрос:
    можно или нельзя выполнить действие.

Важно:
    Permissions не должны изменять данные.
    Изменение состояния выполняется в users/services/.
"""

from apps.users.permissions.admin_user_permissions import (
    CanAccessAdminUsers,
    CanBulkManageAdminUsers,
    CanManageAdminUser,
    CanManageAdminUserRoles,
    CanManageAdminUserStatus,
)
from apps.users.permissions.base import IsActiveUser, IsSuperAdminRole
from apps.users.permissions.guardian_profile_permissions import (
    CanGuardianAccessLearner,
    CanReviewGuardianLink,
)
from apps.users.permissions.helpers import (
    can_review_guardian_link,
    can_review_learner,
    can_review_teacher,
    get_object_context,
    get_object_user,
    has_any_role,
    has_role,
    is_authenticated_active_user,
    is_organization_admin,
    is_organization_reviewer,
    is_safe_method,
    is_self,
    is_superadmin,
)
from apps.users.permissions.invite_code_permissions import (
    CanCreateGuardianLinkCode,
    CanCreateTeacherInviteCode,
    CanDisableInviteCode,
    CanManageInviteCode,
    CanUseInviteCode,
    CanViewInviteCodes,
)
from apps.users.permissions.learner_profile_permissions import (
    CanGuardianViewLearnerProfile,
    CanReviewLearnerProfile,
)
from apps.users.permissions.organization_permissions import IsOrganizationAdminRole
from apps.users.permissions.profile_permissions import (
    CanModerateProfile,
    CanUpdateOwnProfile,
    CanViewProfile,
)
from apps.users.permissions.reviewer_permissions import (
    CanReviewGuardianLinkObject,
    CanReviewLearnerObject,
    CanReviewTeacherObject,
    IsOrganizationReviewerRole,
)
from apps.users.permissions.role_permissions import (
    CanAssignUserRole,
    CanManageSystemRoles,
    CanRevokeUserRole,
    CanViewRoles,
    CanViewUserRole,
)
from apps.users.permissions.teacher_profile_permissions import CanReviewTeacherProfile
from apps.users.permissions.user_permissions import (
    CanAnonymizeUser,
    CanArchiveUser,
    CanBlockUser,
    CanManageUserLifecycle,
    CanManageUsersInOrganization,
    CanReadUserObject,
    CanUpdateUser,
    CanViewOwnOrManagedUser,
    CanViewUser,
)

__all__ = [
    "CanAccessAdminUsers",
    "CanBulkManageAdminUsers",
    "CanManageAdminUser",
    "CanManageAdminUserRoles",
    "CanManageAdminUserStatus",
    "CanAnonymizeUser",
    "CanArchiveUser",
    "CanAssignUserRole",
    "CanBlockUser",
    "CanCreateGuardianLinkCode",
    "CanCreateTeacherInviteCode",
    "CanDisableInviteCode",
    "CanGuardianAccessLearner",
    "CanGuardianViewLearnerProfile",
    "CanManageInviteCode",
    "CanManageSystemRoles",
    "CanManageUserLifecycle",
    "CanManageUsersInOrganization",
    "CanModerateProfile",
    "CanReadUserObject",
    "CanReviewGuardianLink",
    "CanReviewGuardianLinkObject",
    "CanReviewLearnerObject",
    "CanReviewLearnerProfile",
    "CanReviewTeacherObject",
    "CanReviewTeacherProfile",
    "CanRevokeUserRole",
    "CanUpdateOwnProfile",
    "CanUpdateUser",
    "CanUseInviteCode",
    "CanViewInviteCodes",
    "CanViewOwnOrManagedUser",
    "CanViewProfile",
    "CanViewRoles",
    "CanViewUser",
    "CanViewUserRole",
    "IsActiveUser",
    "IsOrganizationAdminRole",
    "IsOrganizationReviewerRole",
    "IsSuperAdminRole",
    "can_review_guardian_link",
    "can_review_learner",
    "can_review_teacher",
    "get_object_context",
    "get_object_user",
    "has_any_role",
    "has_role",
    "is_authenticated_active_user",
    "is_organization_admin",
    "is_organization_reviewer",
    "is_safe_method",
    "is_self",
    "is_superadmin",
]
