from __future__ import annotations

from apps.backoffice.constants import BackofficeUserMessage
from apps.backoffice.selectors.users import actor_can_access_backoffice_user
from apps.users.constants.lifecycle import UserStatus
from apps.users.models import User
from rest_framework.exceptions import PermissionDenied, ValidationError


def validate_backoffice_user_status_access(*, actor, target_user: User) -> None:
    """
    Проверяет, может ли администратор менять статус пользователя.
    """

    if not actor_can_access_backoffice_user(
        actor=actor,
        target_user=target_user,
    ):
        raise PermissionDenied(BackofficeUserMessage.USER_NOT_FOUND_OR_FORBIDDEN)

    if actor and target_user and actor.id == target_user.id:
        raise ValidationError(
            {
                "user": BackofficeUserMessage.SELF_STATUS_CHANGE_FORBIDDEN,
            }
        )


def validate_user_status_is_not_final(*, target_user: User) -> None:
    """
    Проверяет, что пользователь не находится в финальном состоянии.
    """

    if target_user.status == UserStatus.ANONYMIZED or target_user.anonymized_at:
        raise ValidationError(
            {
                "status": BackofficeUserMessage.FINAL_STATUS_FORBIDDEN,
            }
        )


def validate_user_is_not_scheduled_for_deletion(*, target_user: User) -> None:
    """
    Проверяет, что пользователь не запланирован к удалению.
    """

    if (
        target_user.status == UserStatus.SCHEDULED_FOR_DELETION
        or target_user.scheduled_for_deletion_at
    ):
        raise ValidationError(
            {
                "status": (BackofficeUserMessage.USER_ALREADY_SCHEDULED_FOR_DELETION),
            }
        )


def validate_backoffice_user_status_common_rules(
    *,
    actor,
    target_user: User,
    allow_scheduled_for_deletion: bool = False,
) -> None:
    """
    Выполняет общие проверки перед изменением статуса пользователя.
    """

    validate_backoffice_user_status_access(
        actor=actor,
        target_user=target_user,
    )
    validate_user_status_is_not_final(target_user=target_user)

    if not allow_scheduled_for_deletion:
        validate_user_is_not_scheduled_for_deletion(
            target_user=target_user,
        )


# Совместимые alias'ы на время переноса старой admin-user логики.
validate_admin_can_manage_user_status = validate_backoffice_user_status_access
