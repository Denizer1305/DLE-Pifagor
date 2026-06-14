from __future__ import annotations

from .assign import create_or_restore_backoffice_user_role, create_or_restore_user_role
from .change import (
    admin_change_user_roles,
    change_backoffice_user_roles,
    get_role_label_for_notification,
)
from .payloads import (
    AdminRoleAssignmentPayload,
    BackofficeRoleAssignmentPayload,
    normalize_backoffice_role_assignment_payload,
    normalize_role_assignment_payload,
)
from .queries import (
    actor_has_backoffice_department_scope,
    actor_has_backoffice_organization_scope,
    actor_has_department_scope,
    actor_has_organization_scope,
    get_existing_backoffice_user_role_for_assignment,
    get_existing_user_role_for_assignment,
    get_role_for_assignment,
    get_role_for_backoffice_assignment,
)
from .revoke import revoke_backoffice_user_role_by_id, revoke_user_role_by_id
from .validation import (
    PROTECTED_ADMIN_ROLE_CODES,
    PROTECTED_BACKOFFICE_ROLE_CODES,
    validate_actor_can_assign_backoffice_role,
    validate_actor_can_assign_role,
    validate_actor_can_manage_backoffice_target_roles,
    validate_actor_can_manage_target_roles,
    validate_actor_can_revoke_backoffice_user_role,
    validate_actor_can_revoke_user_role,
    validate_target_user_can_receive_backoffice_roles,
    validate_target_user_can_receive_roles,
)

__all__ = [
    "AdminRoleAssignmentPayload",
    "BackofficeRoleAssignmentPayload",
    "PROTECTED_ADMIN_ROLE_CODES",
    "PROTECTED_BACKOFFICE_ROLE_CODES",
    "actor_has_backoffice_department_scope",
    "actor_has_backoffice_organization_scope",
    "actor_has_department_scope",
    "actor_has_organization_scope",
    "admin_change_user_roles",
    "change_backoffice_user_roles",
    "create_or_restore_backoffice_user_role",
    "create_or_restore_user_role",
    "get_existing_backoffice_user_role_for_assignment",
    "get_existing_user_role_for_assignment",
    "get_role_for_assignment",
    "get_role_for_backoffice_assignment",
    "get_role_label_for_notification",
    "normalize_backoffice_role_assignment_payload",
    "normalize_role_assignment_payload",
    "revoke_backoffice_user_role_by_id",
    "revoke_user_role_by_id",
    "validate_actor_can_assign_backoffice_role",
    "validate_actor_can_assign_role",
    "validate_actor_can_manage_backoffice_target_roles",
    "validate_actor_can_manage_target_roles",
    "validate_actor_can_revoke_backoffice_user_role",
    "validate_actor_can_revoke_user_role",
    "validate_target_user_can_receive_backoffice_roles",
    "validate_target_user_can_receive_roles",
]
