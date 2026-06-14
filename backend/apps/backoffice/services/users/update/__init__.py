from __future__ import annotations

from .apply import (
    apply_admin_user_regular_fields,
    apply_backoffice_user_regular_fields,
    get_admin_user_update_fields,
    get_backoffice_user_regular_editable_fields,
    get_backoffice_user_update_fields,
)
from .email import (
    apply_admin_user_email_change,
    apply_backoffice_user_email_change,
    schedule_admin_email_verification_if_needed,
    schedule_backoffice_email_verification_if_needed,
)
from .payloads import (
    extract_backoffice_user_update_service_fields,
    normalize_admin_user_update_data,
    normalize_backoffice_user_update_data,
)
from .save import save_admin_user_update, save_backoffice_user_update
from .service import admin_update_user, update_backoffice_user
from .validation import (
    normalize_expected_updated_at,
    normalize_model_updated_at,
    validate_admin_can_update_user,
    validate_admin_user_expected_updated_at,
    validate_backoffice_user_can_be_updated,
    validate_backoffice_user_expected_updated_at,
    validate_backoffice_user_update_access,
    validate_backoffice_user_update_common_rules,
    validate_target_user_can_be_updated,
)

__all__ = [
    "admin_update_user",
    "apply_admin_user_email_change",
    "apply_admin_user_regular_fields",
    "apply_backoffice_user_email_change",
    "apply_backoffice_user_regular_fields",
    "extract_backoffice_user_update_service_fields",
    "get_admin_user_update_fields",
    "get_backoffice_user_regular_editable_fields",
    "get_backoffice_user_update_fields",
    "normalize_admin_user_update_data",
    "normalize_backoffice_user_update_data",
    "normalize_expected_updated_at",
    "normalize_model_updated_at",
    "save_admin_user_update",
    "save_backoffice_user_update",
    "schedule_admin_email_verification_if_needed",
    "schedule_backoffice_email_verification_if_needed",
    "update_backoffice_user",
    "validate_admin_can_update_user",
    "validate_admin_user_expected_updated_at",
    "validate_backoffice_user_can_be_updated",
    "validate_backoffice_user_expected_updated_at",
    "validate_backoffice_user_update_access",
    "validate_backoffice_user_update_common_rules",
    "validate_target_user_can_be_updated",
]
