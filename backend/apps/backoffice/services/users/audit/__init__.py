from __future__ import annotations

from .events import (
    log_admin_user_archived,
    log_admin_user_blocked,
    log_admin_user_email_changed,
    log_admin_user_restored,
    log_admin_user_roles_changed,
    log_admin_user_scheduled_for_deletion,
    log_admin_user_unblocked,
    log_admin_user_updated,
    log_backoffice_user_archived,
    log_backoffice_user_blocked,
    log_backoffice_user_email_changed,
    log_backoffice_user_restored,
    log_backoffice_user_roles_changed,
    log_backoffice_user_scheduled_for_deletion,
    log_backoffice_user_unblocked,
    log_backoffice_user_updated,
)
from .payloads import (
    ADMIN_USERS_AUDIT_SOURCE,
    BACKOFFICE_USERS_AUDIT_SOURCE,
    build_admin_audit_metadata,
    build_backoffice_user_audit_metadata,
)
from .writer import create_admin_user_audit_log, create_backoffice_user_audit_log

__all__ = [
    "ADMIN_USERS_AUDIT_SOURCE",
    "BACKOFFICE_USERS_AUDIT_SOURCE",
    "build_admin_audit_metadata",
    "build_backoffice_user_audit_metadata",
    "create_admin_user_audit_log",
    "create_backoffice_user_audit_log",
    "log_admin_user_archived",
    "log_admin_user_blocked",
    "log_admin_user_email_changed",
    "log_admin_user_restored",
    "log_admin_user_roles_changed",
    "log_admin_user_scheduled_for_deletion",
    "log_admin_user_unblocked",
    "log_admin_user_updated",
    "log_backoffice_user_archived",
    "log_backoffice_user_blocked",
    "log_backoffice_user_email_changed",
    "log_backoffice_user_restored",
    "log_backoffice_user_roles_changed",
    "log_backoffice_user_scheduled_for_deletion",
    "log_backoffice_user_unblocked",
    "log_backoffice_user_updated",
]
