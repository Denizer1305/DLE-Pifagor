from __future__ import annotations

from apps.backoffice.selectors.users import get_backoffice_users_queryset_for_actor
from apps.backoffice.services.users.update import (
    validate_backoffice_user_expected_updated_at,
)
from apps.core.selectors import get_object_or_none


def get_expected_updated_at_for_user(
    *,
    user_id: int,
    expected_updated_at_map: dict | None = None,
):
    """
    Возвращает expected_updated_at для конкретного пользователя.
    """

    expected_updated_at_map = expected_updated_at_map or {}

    return expected_updated_at_map.get(str(user_id)) or expected_updated_at_map.get(
        user_id
    )


def get_locked_backoffice_user_for_bulk_action(
    *,
    actor,
    user_id: int,
):
    """
    Возвращает пользователя под select_for_update с учётом scope администратора.
    """

    return get_object_or_none(
        get_backoffice_users_queryset_for_actor(actor=actor).select_for_update(),
        id=user_id,
    )


def validate_backoffice_bulk_expected_updated_at(
    *,
    target_user,
    expected_updated_at=None,
) -> None:
    """
    Проверяет optimistic locking для одного пользователя в bulk-операции.
    """

    validate_backoffice_user_expected_updated_at(
        target_user=target_user,
        expected_updated_at=expected_updated_at,
    )


# Совместимые alias'ы.
get_expected_updated_at_for_user = get_expected_updated_at_for_user
get_locked_admin_user_for_bulk_action = get_locked_backoffice_user_for_bulk_action
validate_expected_updated_at = validate_backoffice_bulk_expected_updated_at
