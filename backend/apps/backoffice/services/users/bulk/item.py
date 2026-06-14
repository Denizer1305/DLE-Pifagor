from __future__ import annotations

from apps.backoffice.constants import BackofficeUserBulkAction, BackofficeUserMessage
from apps.backoffice.services.users.bulk.locking import (
    get_expected_updated_at_for_user,
    get_locked_backoffice_user_for_bulk_action,
    validate_backoffice_bulk_expected_updated_at,
)
from apps.backoffice.services.users.bulk.payloads import (
    BackofficeUserBulkItemResult,
    build_failed_bulk_item_result,
    build_success_bulk_item_result,
)
from apps.backoffice.services.users.delete import schedule_backoffice_user_deletion
from apps.backoffice.services.users.roles import change_backoffice_user_roles
from apps.backoffice.services.users.status import (
    archive_backoffice_user,
    block_backoffice_user,
    restore_backoffice_user,
    unblock_backoffice_user,
)
from django.db import transaction
from rest_framework.exceptions import APIException, PermissionDenied, ValidationError


def get_bulk_success_message(*, action: str) -> str:
    """
    Возвращает сообщение успешной bulk-операции.
    """

    messages = {
        BackofficeUserBulkAction.BLOCK: "Пользователь заблокирован.",
        BackofficeUserBulkAction.UNBLOCK: "Пользователь разблокирован.",
        BackofficeUserBulkAction.ARCHIVE: "Пользователь архивирован.",
        BackofficeUserBulkAction.RESTORE: "Пользователь восстановлен.",
        BackofficeUserBulkAction.DELETE: "Удаление пользователя запланировано.",
        BackofficeUserBulkAction.CHANGE_ROLES: "Роли пользователя изменены.",
    }

    return messages.get(action, "Пользователь обработан.")


def perform_backoffice_user_bulk_item_action(
    *,
    actor,
    target_user,
    action: str,
    reason: str = "",
    role_payload: dict | None = None,
    bulk_action_id: str = "",
    request=None,
):
    """
    Выполняет bulk-action для одного пользователя.
    """

    if action == BackofficeUserBulkAction.BLOCK:
        return block_backoffice_user(
            actor=actor,
            target_user=target_user,
            reason=reason,
            bulk_action_id=bulk_action_id,
            request=request,
        )

    if action == BackofficeUserBulkAction.UNBLOCK:
        return unblock_backoffice_user(
            actor=actor,
            target_user=target_user,
            reason=reason,
            bulk_action_id=bulk_action_id,
            request=request,
        )

    if action == BackofficeUserBulkAction.ARCHIVE:
        return archive_backoffice_user(
            actor=actor,
            target_user=target_user,
            reason=reason,
            bulk_action_id=bulk_action_id,
            request=request,
        )

    if action == BackofficeUserBulkAction.RESTORE:
        return restore_backoffice_user(
            actor=actor,
            target_user=target_user,
            reason=reason,
            bulk_action_id=bulk_action_id,
            request=request,
        )

    if action == BackofficeUserBulkAction.DELETE:
        return schedule_backoffice_user_deletion(
            actor=actor,
            target_user=target_user,
            reason=reason,
            bulk_action_id=bulk_action_id,
            request=request,
        )

    if action == BackofficeUserBulkAction.CHANGE_ROLES:
        role_payload = role_payload or {}

        return change_backoffice_user_roles(
            actor=actor,
            target_user=target_user,
            assigned_roles=role_payload.get("assigned_roles") or [],
            revoked_user_role_ids=role_payload.get("revoked_user_role_ids") or [],
            reason=reason or role_payload.get("reason", ""),
            bulk_action_id=bulk_action_id,
            request=request,
        )

    raise ValidationError(
        {
            "action": BackofficeUserMessage.UNSUPPORTED_BULK_ACTION,
        }
    )


def execute_backoffice_user_bulk_item(
    *,
    actor,
    user_id: int,
    action: str,
    reason: str = "",
    role_payload: dict | None = None,
    expected_updated_at_map: dict | None = None,
    bulk_action_id: str = "",
    request=None,
) -> BackofficeUserBulkItemResult:
    """
    Выполняет bulk-action для одного пользователя и возвращает результат.

    Ошибка по одному пользователю не останавливает всю bulk-операцию.
    """

    try:
        with transaction.atomic():
            target_user = get_locked_backoffice_user_for_bulk_action(
                actor=actor,
                user_id=user_id,
            )

            if target_user is None:
                return build_failed_bulk_item_result(
                    user_id=user_id,
                    action=action,
                    message=BackofficeUserMessage.USER_NOT_FOUND_OR_FORBIDDEN,
                    error_code="user_not_found_or_forbidden",
                )

            validate_backoffice_bulk_expected_updated_at(
                target_user=target_user,
                expected_updated_at=get_expected_updated_at_for_user(
                    user_id=user_id,
                    expected_updated_at_map=expected_updated_at_map,
                ),
            )

            perform_backoffice_user_bulk_item_action(
                actor=actor,
                target_user=target_user,
                action=action,
                reason=reason,
                role_payload=role_payload,
                bulk_action_id=bulk_action_id,
                request=request,
            )

            return build_success_bulk_item_result(
                user_id=user_id,
                action=action,
                message=get_bulk_success_message(action=action),
            )

    except (ValidationError, PermissionDenied) as error:
        return build_failed_bulk_item_result(
            user_id=user_id,
            action=action,
            message=str(error.detail),
            error_code=getattr(error, "default_code", "validation_error"),
            errors=error.detail if isinstance(error.detail, dict) else {},
        )

    except APIException as error:
        return build_failed_bulk_item_result(
            user_id=user_id,
            action=action,
            message=str(error.detail),
            error_code=getattr(error, "default_code", "api_error"),
            errors=error.detail if isinstance(error.detail, dict) else {},
        )


# Совместимые alias'ы.
perform_admin_user_bulk_item_action = perform_backoffice_user_bulk_item_action
execute_admin_user_bulk_item = execute_backoffice_user_bulk_item
