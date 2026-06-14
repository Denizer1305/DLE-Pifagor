from __future__ import annotations

from apps.backoffice.services.users.audit import (
    log_backoffice_user_blocked,
    log_backoffice_user_unblocked,
)
from apps.backoffice.services.users.status.restore import get_restored_user_status
from apps.backoffice.services.users.status.validation import (
    validate_backoffice_user_status_common_rules,
)
from apps.core.services import save_model
from apps.users.constants.lifecycle import UserStatus
from apps.users.models import User
from apps.users.tasks.email_tasks import send_account_unblocked_task
from django.db import transaction
from rest_framework.exceptions import ValidationError


def block_backoffice_user(
    *,
    actor,
    target_user: User,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
) -> User:
    """
    Блокирует пользователя из backoffice.
    """

    validate_backoffice_user_status_common_rules(
        actor=actor,
        target_user=target_user,
    )

    if target_user.status == UserStatus.BLOCKED:
        raise ValidationError(
            {
                "status": "Пользователь уже заблокирован.",
            }
        )

    target_user.status = UserStatus.BLOCKED
    target_user.is_active = False

    save_model(
        target_user,
        update_fields=[
            "status",
            "is_active",
        ],
    )

    log_backoffice_user_blocked(
        actor=actor,
        target_user=target_user,
        reason=reason,
        bulk_action_id=bulk_action_id,
        request=request,
    )

    return target_user


def unblock_backoffice_user(
    *,
    actor,
    target_user: User,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
) -> User:
    """
    Разблокирует пользователя из backoffice.
    """

    validate_backoffice_user_status_common_rules(
        actor=actor,
        target_user=target_user,
    )

    if target_user.status != UserStatus.BLOCKED:
        raise ValidationError(
            {
                "status": (
                    "Разблокировать можно только заблокированного пользователя."
                ),
            }
        )

    target_user.status = get_restored_user_status(target_user=target_user)
    target_user.is_active = target_user.status == UserStatus.ACTIVE

    save_model(
        target_user,
        update_fields=[
            "status",
            "is_active",
        ],
    )

    log_backoffice_user_unblocked(
        actor=actor,
        target_user=target_user,
        reason=reason,
        bulk_action_id=bulk_action_id,
        request=request,
    )

    transaction.on_commit(
        lambda: send_account_unblocked_task.delay(
            user_id=target_user.id,
            reason=reason,
        )
    )

    return target_user


# Совместимые alias'ы на время переноса старой admin-user логики.
admin_block_user = block_backoffice_user
admin_unblock_user = unblock_backoffice_user
