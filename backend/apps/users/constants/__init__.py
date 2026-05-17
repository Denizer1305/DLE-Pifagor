"""
Константы приложения users.

Здесь экспортируются:
    - роли;
    - статусы жизненного цикла;
    - статусы профилей;
    - типы заявок;
    - типы кодов приглашения;
    - статусы модерации;
    - события аудита.
"""

from apps.users.constants.audit import (
    JOIN_REQUEST_AUDIT_ACTIONS,
    LIFECYCLE_AUDIT_ACTIONS,
    SECURITY_AUDIT_ACTIONS,
    AuditActorType,
    AuditObjectType,
    UserAuditAction,
)
from apps.users.constants.lifecycle import (
    ACTIVE_GUARDIAN_LEARNER_STATUSES,
    ACTIVE_ROLE_STATUSES,
    ACTIVE_USER_STATUSES,
    DELETION_CANDIDATE_USER_STATUSES,
    FINAL_USER_STATUSES,
    INACTIVE_ROLE_STATUSES,
    INACTIVE_USER_STATUSES,
    VERIFIED_PROFILE_STATUSES,
    GuardianLearnerStatus,
    ProfileStatus,
    UserRoleStatus,
    UserStatus,
)
from apps.users.constants.moderation import (
    APPROVED_MODERATION_STATUSES,
    PENDING_MODERATION_STATUSES,
    REJECTED_MODERATION_STATUSES,
    ModerationDecision,
    ModerationStatus,
    ModerationTarget,
)
from apps.users.constants.onboarding import (
    ACTIVE_INVITE_CODE_PURPOSES,
    DEFAULT_GUARDIAN_LINK_CODE_TTL_HOURS,
    DEFAULT_INVITE_CODE_LENGTH,
    DEFAULT_INVITE_CODE_TTL_HOURS,
    FINAL_JOIN_REQUEST_STATUSES,
    GUARDIAN_LINK_INVITE_CODE_PURPOSES,
    PENDING_JOIN_REQUEST_STATUSES,
    REGISTRATION_ATTEMPT_LIMIT,
    REGISTRATION_ATTEMPT_WINDOW_MINUTES,
    InviteCodePurpose,
    JoinRequestStatus,
    JoinRequestType,
    RegistrationAttemptStatus,
    RegistrationFailureReason,
)
from apps.users.constants.roles import (
    GUARDIAN_REVIEWER_ROLE_CODES,
    GUARDIAN_ROLE_CODES,
    LEARNER_REVIEWER_ROLE_CODES,
    LEARNER_ROLE_CODES,
    ORGANIZATION_ADMIN_ROLE_CODES,
    ORGANIZATION_REVIEWER_ROLE_CODES,
    PLATFORM_ADMIN_ROLE_CODES,
    ROLE_LABELS,
    ROLE_SORT_ORDER,
    STAFF_ROLE_CODES,
    TEACHER_REVIEWER_ROLE_CODES,
    RoleCode,
)

__all__ = [
    "ACTIVE_GUARDIAN_LEARNER_STATUSES",
    "ACTIVE_INVITE_CODE_PURPOSES",
    "ACTIVE_ROLE_STATUSES",
    "ACTIVE_USER_STATUSES",
    "APPROVED_MODERATION_STATUSES",
    "AuditActorType",
    "AuditObjectType",
    "DELETION_CANDIDATE_USER_STATUSES",
    "DEFAULT_GUARDIAN_LINK_CODE_TTL_HOURS",
    "DEFAULT_INVITE_CODE_LENGTH",
    "DEFAULT_INVITE_CODE_TTL_HOURS",
    "FINAL_JOIN_REQUEST_STATUSES",
    "FINAL_USER_STATUSES",
    "GUARDIAN_LINK_INVITE_CODE_PURPOSES",
    "GUARDIAN_REVIEWER_ROLE_CODES",
    "GUARDIAN_ROLE_CODES",
    "GuardianLearnerStatus",
    "INACTIVE_ROLE_STATUSES",
    "INACTIVE_USER_STATUSES",
    "InviteCodePurpose",
    "JOIN_REQUEST_AUDIT_ACTIONS",
    "JoinRequestStatus",
    "JoinRequestType",
    "LEARNER_REVIEWER_ROLE_CODES",
    "LEARNER_ROLE_CODES",
    "LIFECYCLE_AUDIT_ACTIONS",
    "ModerationDecision",
    "ModerationStatus",
    "ModerationTarget",
    "ORGANIZATION_ADMIN_ROLE_CODES",
    "ORGANIZATION_REVIEWER_ROLE_CODES",
    "PENDING_JOIN_REQUEST_STATUSES",
    "PENDING_MODERATION_STATUSES",
    "PLATFORM_ADMIN_ROLE_CODES",
    "ProfileStatus",
    "REGISTRATION_ATTEMPT_LIMIT",
    "REGISTRATION_ATTEMPT_WINDOW_MINUTES",
    "REJECTED_MODERATION_STATUSES",
    "ROLE_LABELS",
    "ROLE_SORT_ORDER",
    "RegistrationAttemptStatus",
    "RegistrationFailureReason",
    "RoleCode",
    "SECURITY_AUDIT_ACTIONS",
    "STAFF_ROLE_CODES",
    "TEACHER_REVIEWER_ROLE_CODES",
    "UserAuditAction",
    "UserRoleStatus",
    "UserStatus",
    "VERIFIED_PROFILE_STATUSES",
]
