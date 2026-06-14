from __future__ import annotations

from apps.backoffice.services.users.bulk.item import execute_backoffice_user_bulk_item
from apps.backoffice.services.users.bulk.payloads import BackofficeUserBulkResult
from apps.backoffice.services.users.bulk.validation import (
    validate_backoffice_bulk_common_rules,
)
from apps.core.utils import generate_uuid_string


def execute_backoffice_users_bulk_action(
    *,
    actor,
    action: str,
    user_ids: list[int] | tuple[int, ...] | set[int],
    reason: str = "",
    role_payload: dict | None = None,
    expected_updated_at_map: dict | None = None,
    request=None,
) -> BackofficeUserBulkResult:
    """
    Выполняет массовое действие над пользователями.

    Операция не падает целиком из-за ошибки одного пользователя.
    Каждый пользователь получает отдельный результат обработки.
    """

    normalized_user_ids = validate_backoffice_bulk_common_rules(
        action=action,
        user_ids=user_ids,
        role_payload=role_payload,
    )
    bulk_action_id = generate_uuid_string()

    items = [
        execute_backoffice_user_bulk_item(
            actor=actor,
            user_id=user_id,
            action=action,
            reason=reason,
            role_payload=role_payload,
            expected_updated_at_map=expected_updated_at_map,
            bulk_action_id=bulk_action_id,
            request=request,
        )
        for user_id in normalized_user_ids
    ]

    return BackofficeUserBulkResult(
        action=action,
        items=items,
        bulk_action_id=bulk_action_id,
    )


# Совместимый alias.
execute_admin_users_bulk_action = execute_backoffice_users_bulk_action
