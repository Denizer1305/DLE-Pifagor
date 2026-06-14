from __future__ import annotations

from apps.backoffice.constants import BackofficeUserMessage
from apps.backoffice.selectors.users import actor_can_access_backoffice_user
from apps.users.constants.lifecycle import UserStatus
from apps.users.models import User
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied, ValidationError


def validate_backoffice_user_delete_access(*, actor, target_user: User) -> None:
    """
    Проверяет, может ли администратор планировать удаление пользователя.
    """

    if not actor_can_access_backoffice_user(
        actor=actor,
        target_user=target_user,
    ):
        raise PermissionDenied(BackofficeUserMessage.USER_NOT_FOUND_OR_FORBIDDEN)

    if actor and target_user and actor.id == target_user.id:
        raise ValidationError(
            {
                "user": BackofficeUserMessage.SELF_DELETE_FORBIDDEN,
            }
        )


def validate_backoffice_user_can_be_scheduled_for_deletion(
    *,
    target_user: User,
) -> None:
    """
    Проверяет, можно ли запланировать удаление пользователя.
    """

    if target_user.status == UserStatus.ANONYMIZED or target_user.anonymized_at:
        raise ValidationError(
            {
                "status": BackofficeUserMessage.FINAL_STATUS_FORBIDDEN,
            }
        )

    if (
        target_user.status == UserStatus.SCHEDULED_FOR_DELETION
        or target_user.scheduled_for_deletion_at
    ):
        raise ValidationError(
            {
                "status": (BackofficeUserMessage.USER_ALREADY_SCHEDULED_FOR_DELETION),
            }
        )


def validate_scheduled_for_deletion_at(value) -> None:
    """
    Проверяет дату планируемого удаления.
    """

    if value is None:
        return

    if value <= timezone.now():
        raise ValidationError(
            {
                "scheduled_for_deletion_at": ("Дата удаления должна быть в будущем."),
            }
        )


def validate_backoffice_user_delete_common_rules(
    *,
    actor,
    target_user: User,
    scheduled_for_deletion_at=None,
) -> None:
    """
    Выполняет общие проверки перед планированием удаления.
    """

    validate_backoffice_user_delete_access(
        actor=actor,
        target_user=target_user,
    )
    validate_backoffice_user_can_be_scheduled_for_deletion(
        target_user=target_user,
    )
    validate_scheduled_for_deletion_at(scheduled_for_deletion_at)


# Совместимый alias на время переноса старой admin-user логики.
validate_admin_can_delete_user = validate_backoffice_user_delete_access
