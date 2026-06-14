from __future__ import annotations


class BackofficeUserErrorCode:
    """
    Машинные коды ошибок административного управления пользователями.
    """

    USER_NOT_FOUND = "backoffice_user_not_found"
    USER_FORBIDDEN = "backoffice_user_forbidden"
    SELF_STATUS_CHANGE_FORBIDDEN = "self_status_change_forbidden"
    SELF_DELETE_FORBIDDEN = "self_delete_forbidden"
    FINAL_STATUS_FORBIDDEN = "final_status_forbidden"
    USER_ALREADY_BLOCKED = "user_already_blocked"
    USER_ALREADY_ACTIVE = "user_already_active"
    USER_ALREADY_ARCHIVED = "user_already_archived"
    USER_ALREADY_SCHEDULED_FOR_DELETION = "user_already_scheduled_for_deletion"
    STALE_OBJECT = "stale_object"
    UNSUPPORTED_BULK_ACTION = "unsupported_bulk_action"
    EMPTY_BULK_USER_IDS = "empty_bulk_user_ids"
    ROLE_NOT_FOUND = "role_not_found"
    ROLE_NOT_AVAILABLE = "role_not_available"
    ROLE_ALREADY_ASSIGNED = "role_already_assigned"
    ROLE_ASSIGNMENT_FORBIDDEN = "role_assignment_forbidden"
    ROLE_REVOKE_FORBIDDEN = "role_revoke_forbidden"
