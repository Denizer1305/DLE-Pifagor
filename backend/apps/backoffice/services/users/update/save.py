from __future__ import annotations

from apps.core.services import save_model
from apps.users.models import User
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError


def save_backoffice_user_update(
    *,
    target_user: User,
    update_fields: list[str],
) -> None:
    """
    Валидирует и сохраняет пользователя.
    """

    if not update_fields:
        return

    try:
        target_user.full_clean()
        save_model(
            target_user,
            update_fields=update_fields,
        )
    except IntegrityError as error:
        raise ValidationError(
            {
                "detail": (
                    "Не удалось сохранить пользователя. Возможно, email или "
                    "телефон уже используются другим пользователем."
                )
            }
        ) from error


# Совместимый alias на время переноса старой admin-user логики.
save_admin_user_update = save_backoffice_user_update
