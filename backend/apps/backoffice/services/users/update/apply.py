from __future__ import annotations

from typing import Any

from apps.backoffice.constants import BACKOFFICE_USER_EDITABLE_FIELDS
from apps.core.services import apply_model_fields
from apps.users.models import User

EMAIL_FIELD_NAME = "email"


def get_backoffice_user_regular_editable_fields() -> set[str]:
    """
    Возвращает обычные редактируемые поля без email.

    Email обрабатывается отдельно, потому что его изменение сбрасывает
    подтверждение почты и меняет status.
    """

    return set(BACKOFFICE_USER_EDITABLE_FIELDS) - {EMAIL_FIELD_NAME}


def apply_backoffice_user_regular_fields(
    *,
    target_user: User,
    data: dict[str, Any],
) -> list[str]:
    """
    Применяет обычные редактируемые поля пользователя.

    Не применяет email — для него есть отдельный helper.
    """

    return apply_model_fields(
        instance=target_user,
        data=data,
        allowed_fields=get_backoffice_user_regular_editable_fields(),
    )


def get_backoffice_user_update_fields(
    *,
    changed_fields: list[str],
    email_changed: bool,
) -> list[str]:
    """
    Формирует список полей для user.save(update_fields=...).
    """

    update_fields = list(changed_fields)

    if email_changed:
        update_fields.extend(
            [
                "email",
                "is_email_verified",
                "email_verified_at",
                "status",
                "is_active",
            ]
        )

    return list(dict.fromkeys(update_fields))


# Совместимые alias'ы на время переноса старой admin-user логики.
apply_admin_user_regular_fields = apply_backoffice_user_regular_fields
get_admin_user_update_fields = get_backoffice_user_update_fields
