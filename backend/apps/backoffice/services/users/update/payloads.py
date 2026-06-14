from __future__ import annotations

from typing import Any

from apps.backoffice.constants import (
    BACKOFFICE_USER_EDITABLE_FIELDS,
    BACKOFFICE_USER_SERVICE_ONLY_FIELDS,
)


def normalize_backoffice_user_update_data(*, data: dict[str, Any]) -> dict[str, Any]:
    """
    Очищает payload редактирования пользователя.

    Возвращает только поля, которые разрешено менять через backoffice update.
    """

    normalized_data: dict[str, Any] = {}

    for field_name in BACKOFFICE_USER_EDITABLE_FIELDS:
        if field_name in data:
            normalized_data[field_name] = data[field_name]

    return normalized_data


def extract_backoffice_user_update_service_fields(
    *,
    data: dict[str, Any],
) -> dict[str, Any]:
    """
    Возвращает служебные поля update-сервиса.

    Эти поля не пишутся напрямую в User.
    """

    return {
        field_name: data[field_name]
        for field_name in BACKOFFICE_USER_SERVICE_ONLY_FIELDS
        if field_name in data
    }


# Совместимые alias'ы на время переноса старой admin-user логики.
normalize_admin_user_update_data = normalize_backoffice_user_update_data
