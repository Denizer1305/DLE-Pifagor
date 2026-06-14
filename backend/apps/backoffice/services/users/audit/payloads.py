from __future__ import annotations

from typing import Any

BACKOFFICE_USERS_AUDIT_SOURCE = "backoffice_users"
"""
Источник audit-событий административного управления пользователями.
"""


def build_backoffice_user_audit_metadata(
    *,
    metadata: dict[str, Any] | None = None,
    reason: str = "",
    bulk_action_id: str = "",
) -> dict[str, Any]:
    """
    Собирает metadata для audit-событий backoffice users.
    """

    audit_metadata = {
        "source": BACKOFFICE_USERS_AUDIT_SOURCE,
    }

    if reason:
        audit_metadata["reason"] = reason

    if bulk_action_id:
        audit_metadata["bulk_action_id"] = bulk_action_id

    if metadata:
        audit_metadata.update(metadata)

    return audit_metadata


# Совместимый alias на время переноса старой admin-user логики.
ADMIN_USERS_AUDIT_SOURCE = BACKOFFICE_USERS_AUDIT_SOURCE
build_admin_audit_metadata = build_backoffice_user_audit_metadata
