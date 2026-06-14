from __future__ import annotations

from typing import Any

from apps.backoffice.services.users.audit.payloads import (
    build_backoffice_user_audit_metadata,
)
from apps.users.constants.audit import AuditActorType
from apps.users.services.audit_services import create_user_audit_log


def create_backoffice_user_audit_log(
    *,
    action: str,
    actor,
    target_user,
    message: str = "",
    reason: str = "",
    metadata: dict[str, Any] | None = None,
    bulk_action_id: str = "",
    request=None,
):
    """
    Создаёт audit-запись административного действия над пользователем.
    """

    return create_user_audit_log(
        action=action,
        actor=actor,
        target_user=target_user,
        actor_type=AuditActorType.ADMIN,
        message=message,
        metadata=build_backoffice_user_audit_metadata(
            metadata=metadata,
            reason=reason,
            bulk_action_id=bulk_action_id,
        ),
        request=request,
    )


# Совместимый alias на время переноса старой admin-user логики.
create_admin_user_audit_log = create_backoffice_user_audit_log
