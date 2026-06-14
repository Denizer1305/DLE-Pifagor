from __future__ import annotations

from apps.backoffice.services.users.audit import (
    log_backoffice_user_scheduled_for_deletion,
)
from apps.backoffice.services.users.delete.validation import (
    validate_backoffice_user_delete_common_rules,
)
from apps.core.constants import DEFAULT_DELETION_GRACE_DAYS
from apps.core.services import save_model
from apps.core.utils import now_plus_days
from apps.users.constants.lifecycle import UserStatus
from apps.users.models import User
from django.db import transaction


def get_default_scheduled_for_deletion_at():
    """
    Возвращает дату удаления по умолчанию.

    По правилу проекта пользователь сначала переводится в состояние
    scheduled_for_deletion, а фактическое удаление/анонимизация выполняется
    позднее.
    """

    return now_plus_days(DEFAULT_DELETION_GRACE_DAYS)


def schedule_backoffice_user_deletion(
    *,
    actor,
    target_user: User,
    reason: str = "",
    scheduled_for_deletion_at=None,
    bulk_action_id: str = "",
    request=None,
) -> User:
    """
    Планирует удаление пользователя из backoffice.
    """

    scheduled_for_deletion_at = (
        scheduled_for_deletion_at or get_default_scheduled_for_deletion_at()
    )

    validate_backoffice_user_delete_common_rules(
        actor=actor,
        target_user=target_user,
        scheduled_for_deletion_at=scheduled_for_deletion_at,
    )

    target_user.status = UserStatus.SCHEDULED_FOR_DELETION
    target_user.is_active = False
    target_user.scheduled_for_deletion_at = scheduled_for_deletion_at

    save_model(
        target_user,
        update_fields=[
            "status",
            "is_active",
            "scheduled_for_deletion_at",
        ],
    )

    log_backoffice_user_scheduled_for_deletion(
        actor=actor,
        target_user=target_user,
        scheduled_for_deletion_at=scheduled_for_deletion_at,
        reason=reason,
        bulk_action_id=bulk_action_id,
        request=request,
    )

    transaction.on_commit(lambda: None)

    return target_user


# Совместимые alias'ы на время переноса старой admin-user логики.
admin_schedule_user_deletion = schedule_backoffice_user_deletion
schedule_admin_user_deletion = schedule_backoffice_user_deletion
