from __future__ import annotations

from .execution import (
    execute_admin_users_bulk_action,
    execute_backoffice_users_bulk_action,
)
from .item import (
    execute_admin_user_bulk_item,
    execute_backoffice_user_bulk_item,
    get_bulk_success_message,
    perform_admin_user_bulk_item_action,
    perform_backoffice_user_bulk_item_action,
)
from .locking import (
    get_expected_updated_at_for_user,
    get_locked_admin_user_for_bulk_action,
    get_locked_backoffice_user_for_bulk_action,
    validate_backoffice_bulk_expected_updated_at,
    validate_expected_updated_at,
)
from .payloads import (
    AdminUserBulkItemResult,
    AdminUserBulkResult,
    BackofficeUserBulkItemResult,
    BackofficeUserBulkResult,
    build_failed_bulk_item_result,
    build_success_bulk_item_result,
)
from .validation import (
    normalize_backoffice_bulk_user_ids,
    normalize_bulk_user_ids,
    validate_backoffice_bulk_action,
    validate_backoffice_bulk_common_rules,
    validate_backoffice_bulk_role_payload,
    validate_bulk_action,
)

__all__ = [
    "AdminUserBulkItemResult",
    "AdminUserBulkResult",
    "BackofficeUserBulkItemResult",
    "BackofficeUserBulkResult",
    "build_failed_bulk_item_result",
    "build_success_bulk_item_result",
    "execute_admin_user_bulk_item",
    "execute_admin_users_bulk_action",
    "execute_backoffice_user_bulk_item",
    "execute_backoffice_users_bulk_action",
    "get_bulk_success_message",
    "get_expected_updated_at_for_user",
    "get_locked_admin_user_for_bulk_action",
    "get_locked_backoffice_user_for_bulk_action",
    "normalize_backoffice_bulk_user_ids",
    "normalize_bulk_user_ids",
    "perform_admin_user_bulk_item_action",
    "perform_backoffice_user_bulk_item_action",
    "validate_backoffice_bulk_action",
    "validate_backoffice_bulk_common_rules",
    "validate_backoffice_bulk_expected_updated_at",
    "validate_backoffice_bulk_role_payload",
    "validate_bulk_action",
    "validate_expected_updated_at",
]
