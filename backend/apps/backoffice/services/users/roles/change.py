from __future__ import annotations

from apps.backoffice.services.users.audit import log_backoffice_user_roles_changed
from apps.backoffice.services.users.roles.assign import (
    create_or_restore_backoffice_user_role,
)
from apps.backoffice.services.users.roles.payloads import (
    normalize_backoffice_role_assignment_payload,
)
from apps.backoffice.services.users.roles.queries import (
    get_role_for_backoffice_assignment,
)
from apps.backoffice.services.users.roles.revoke import (
    revoke_backoffice_user_role_by_id,
)
from apps.backoffice.services.users.roles.validation import (
    validate_actor_can_assign_backoffice_role,
    validate_actor_can_manage_backoffice_target_roles,
    validate_target_user_can_receive_backoffice_roles,
)
from apps.users.models import User
from apps.users.tasks.email_tasks import send_user_roles_changed_task
from django.db import transaction
from rest_framework.exceptions import ValidationError


def get_role_label_for_notification(user_role) -> str:
    """
    Возвращает название роли для уведомления.
    """

    return getattr(user_role.role, "label", "") or str(user_role.role)


@transaction.atomic
def change_backoffice_user_roles(
    *,
    actor,
    target_user: User,
    assigned_roles: list[dict] | None = None,
    revoked_user_role_ids: list[int] | None = None,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
) -> dict:
    """
    Изменяет роли пользователя из backoffice.
    """

    assigned_roles = assigned_roles or []
    revoked_user_role_ids = revoked_user_role_ids or []

    if not assigned_roles and not revoked_user_role_ids:
        raise ValidationError(
            {
                "roles": "Нужно передать роли для назначения или отзыва.",
            }
        )

    validate_actor_can_manage_backoffice_target_roles(
        actor=actor,
        target_user=target_user,
    )
    validate_target_user_can_receive_backoffice_roles(
        target_user=target_user,
    )

    created_or_restored_user_roles = []
    revoked_user_roles = []

    for raw_payload in assigned_roles:
        payload = normalize_backoffice_role_assignment_payload(raw_payload)
        role = get_role_for_backoffice_assignment(role_id=payload.role_id)

        validate_actor_can_assign_backoffice_role(
            actor=actor,
            role=role,
            payload=payload,
        )

        user_role = create_or_restore_backoffice_user_role(
            actor=actor,
            target_user=target_user,
            role=role,
            payload=payload,
            reason=reason,
        )
        created_or_restored_user_roles.append(user_role)

    for user_role_id in revoked_user_role_ids:
        revoked_user_role = revoke_backoffice_user_role_by_id(
            actor=actor,
            target_user=target_user,
            user_role_id=user_role_id,
            reason=reason,
        )
        revoked_user_roles.append(revoked_user_role)

    log_backoffice_user_roles_changed(
        actor=actor,
        target_user=target_user,
        assigned_role_ids=[
            user_role.role_id for user_role in created_or_restored_user_roles
        ],
        revoked_user_role_ids=[user_role.id for user_role in revoked_user_roles],
        reason=reason,
        bulk_action_id=bulk_action_id,
        request=request,
    )

    transaction.on_commit(
        lambda: send_user_roles_changed_task.delay(
            user_id=target_user.id,
            assigned_roles_text=", ".join(
                get_role_label_for_notification(user_role)
                for user_role in created_or_restored_user_roles
            ),
            revoked_roles_text=", ".join(
                get_role_label_for_notification(user_role)
                for user_role in revoked_user_roles
            ),
        ),
    )

    return {
        "assigned_user_role_ids": [
            user_role.id for user_role in created_or_restored_user_roles
        ],
        "revoked_user_role_ids": [user_role.id for user_role in revoked_user_roles],
    }


# Совместимый alias.
admin_change_user_roles = change_backoffice_user_roles
