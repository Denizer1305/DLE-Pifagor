from __future__ import annotations

from apps.backoffice.services.users.audit import (
    log_backoffice_user_archived,
    log_backoffice_user_restored,
)
from apps.backoffice.services.users.status.restore import (
    clear_user_archive_fields,
    get_restored_user_status,
)
from apps.backoffice.services.users.status.validation import (
    validate_backoffice_user_status_common_rules,
)
from apps.core.services import save_model
from apps.users.constants.lifecycle import UserStatus
from apps.users.models import User
from apps.users.tasks.email_tasks import (
    send_account_archived_task,
    send_account_restored_task,
)
from django.db import transaction
from rest_framework.exceptions import ValidationError


def archive_backoffice_user(
    *,
    actor,
    target_user: User,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
) -> User:
    """
    Архивирует пользователя из backoffice.
    """

    validate_backoffice_user_status_common_rules(
        actor=actor,
        target_user=target_user,
    )

    if target_user.status == UserStatus.ARCHIVED:
        raise ValidationError(
            {
                "status": "Пользователь уже находится в архиве.",
            }
        )

    target_user.status = UserStatus.ARCHIVED
    target_user.is_active = False

    if hasattr(target_user, "archive"):
        target_user.archive(
            user=actor,
            reason=reason,
            save=False,
        )

    save_model(
        target_user,
        update_fields=[
            "status",
            "is_active",
            "archived_at",
            "archived_by",
            "archive_reason",
        ],
    )

    log_backoffice_user_archived(
        actor=actor,
        target_user=target_user,
        reason=reason,
        bulk_action_id=bulk_action_id,
        request=request,
    )

    transaction.on_commit(
        lambda: send_account_archived_task.delay(
            user_id=target_user.id,
            reason=reason,
        )
    )

    return target_user


def restore_backoffice_user(
    *,
    actor,
    target_user: User,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
) -> User:
    """
    Восстанавливает пользователя из архива, блокировки или удаления.
    """

    validate_backoffice_user_status_common_rules(
        actor=actor,
        target_user=target_user,
        allow_scheduled_for_deletion=True,
    )

    previous_status = target_user.status
    allowed_statuses = {
        UserStatus.BLOCKED,
        UserStatus.ARCHIVED,
        UserStatus.SCHEDULED_FOR_DELETION,
    }

    if (
        previous_status not in allowed_statuses
        and not target_user.scheduled_for_deletion_at
    ):
        raise ValidationError(
            {
                "status": (
                    "Восстановить можно только заблокированного, архивного "
                    "или запланированного к удалению пользователя."
                ),
            }
        )

    target_user.status = get_restored_user_status(target_user=target_user)
    target_user.is_active = target_user.status == UserStatus.ACTIVE
    target_user.scheduled_for_deletion_at = None

    update_fields = [
        "status",
        "is_active",
        "scheduled_for_deletion_at",
    ]
    update_fields.extend(clear_user_archive_fields(target_user=target_user))

    save_model(
        target_user,
        update_fields=update_fields,
    )

    log_backoffice_user_restored(
        actor=actor,
        target_user=target_user,
        previous_status=previous_status,
        reason=reason,
        bulk_action_id=bulk_action_id,
        request=request,
    )

    transaction.on_commit(
        lambda: send_account_restored_task.delay(
            user_id=target_user.id,
            previous_status=previous_status,
            reason=reason,
        )
    )

    return target_user


# Совместимые alias'ы на время переноса старой admin-user логики.
admin_archive_user = archive_backoffice_user
admin_restore_user = restore_backoffice_user
