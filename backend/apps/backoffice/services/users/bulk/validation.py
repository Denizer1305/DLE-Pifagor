from __future__ import annotations

from apps.backoffice.constants import BackofficeUserBulkAction, BackofficeUserMessage
from rest_framework.exceptions import ValidationError


def validate_backoffice_bulk_action(*, action: str) -> None:
    """
    Проверяет, что bulk-action поддерживается.
    """

    if action not in BackofficeUserBulkAction.CHOICES:
        raise ValidationError(
            {
                "action": BackofficeUserMessage.UNSUPPORTED_BULK_ACTION,
            }
        )


def normalize_backoffice_bulk_user_ids(
    *,
    user_ids: list[int] | tuple[int, ...] | set[int],
) -> list[int]:
    """
    Нормализует список ID пользователей для bulk-операции.
    """

    normalized_user_ids = list(dict.fromkeys(int(user_id) for user_id in user_ids))

    if not normalized_user_ids:
        raise ValidationError(
            {
                "user_ids": BackofficeUserMessage.EMPTY_BULK_USER_IDS,
            }
        )

    return normalized_user_ids


def validate_backoffice_bulk_role_payload(
    *,
    action: str,
    role_payload: dict | None = None,
) -> None:
    """
    Проверяет совместимость role_payload и bulk-action.
    """

    if action == BackofficeUserBulkAction.CHANGE_ROLES and not role_payload:
        raise ValidationError(
            {
                "role_payload": BackofficeUserMessage.ROLE_PAYLOAD_REQUIRED,
            }
        )

    if action != BackofficeUserBulkAction.CHANGE_ROLES and role_payload:
        raise ValidationError(
            {
                "role_payload": BackofficeUserMessage.ROLE_PAYLOAD_FORBIDDEN,
            }
        )


def validate_backoffice_bulk_common_rules(
    *,
    action: str,
    user_ids: list[int] | tuple[int, ...] | set[int],
    role_payload: dict | None = None,
) -> list[int]:
    """
    Выполняет общие проверки bulk-операции.
    """

    validate_backoffice_bulk_action(action=action)
    validate_backoffice_bulk_role_payload(
        action=action,
        role_payload=role_payload,
    )

    return normalize_backoffice_bulk_user_ids(user_ids=user_ids)


# Совместимые alias'ы.
validate_bulk_action = validate_backoffice_bulk_action
normalize_bulk_user_ids = normalize_backoffice_bulk_user_ids
