from __future__ import annotations

from datetime import datetime

from apps.backoffice.constants import BackofficeUserMessage
from apps.backoffice.selectors.users import actor_can_access_backoffice_user
from apps.users.constants.lifecycle import UserStatus
from apps.users.models import User
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework.exceptions import PermissionDenied, ValidationError


def validate_backoffice_user_update_access(*, actor, target_user: User) -> None:
    """
    Проверяет, может ли администратор редактировать пользователя.
    """

    if not actor_can_access_backoffice_user(
        actor=actor,
        target_user=target_user,
    ):
        raise PermissionDenied(BackofficeUserMessage.USER_NOT_FOUND_OR_FORBIDDEN)


def validate_backoffice_user_can_be_updated(*, target_user: User) -> None:
    """
    Проверяет, можно ли редактировать пользователя.
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


def normalize_expected_updated_at(value: str | datetime | None):
    """
    Нормализует expected_updated_at для optimistic locking.
    """

    if not value:
        return None

    parsed_value = value if isinstance(value, datetime) else parse_datetime(value)

    if parsed_value is None:
        raise ValidationError(
            {
                "expected_updated_at": "Некорректный формат даты обновления.",
            }
        )

    if timezone.is_naive(parsed_value):
        return timezone.make_aware(
            parsed_value,
            timezone.get_current_timezone(),
        )

    return parsed_value


def normalize_model_updated_at(value):
    """
    Нормализует updated_at модели для сравнения.
    """

    if value and timezone.is_naive(value):
        return timezone.make_aware(
            value,
            timezone.get_current_timezone(),
        )

    return value


def validate_backoffice_user_expected_updated_at(
    *,
    target_user: User,
    expected_updated_at: str | datetime | None = None,
) -> None:
    """
    Проверяет optimistic locking по updated_at.

    Если frontend передал expected_updated_at и он не совпадает с текущим
    updated_at пользователя, значит запись уже изменил другой администратор.
    """

    parsed_expected_updated_at = normalize_expected_updated_at(expected_updated_at)

    if parsed_expected_updated_at is None:
        return

    current_updated_at = normalize_model_updated_at(target_user.updated_at)

    if current_updated_at != parsed_expected_updated_at:
        raise ValidationError(
            {
                "expected_updated_at": BackofficeUserMessage.STALE_OBJECT,
            }
        )


def validate_backoffice_user_update_common_rules(
    *,
    actor,
    target_user: User,
    expected_updated_at: str | datetime | None = None,
) -> None:
    """
    Выполняет общие проверки перед обновлением пользователя.
    """

    validate_backoffice_user_update_access(
        actor=actor,
        target_user=target_user,
    )
    validate_backoffice_user_can_be_updated(
        target_user=target_user,
    )
    validate_backoffice_user_expected_updated_at(
        target_user=target_user,
        expected_updated_at=expected_updated_at,
    )


# Совместимые alias'ы на время переноса старой admin-user логики.
validate_admin_can_update_user = validate_backoffice_user_update_access
validate_target_user_can_be_updated = validate_backoffice_user_can_be_updated
validate_admin_user_expected_updated_at = validate_backoffice_user_expected_updated_at
