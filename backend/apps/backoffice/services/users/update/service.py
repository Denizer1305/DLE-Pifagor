from __future__ import annotations

from typing import Any

from apps.backoffice.services.users.audit import (
    log_backoffice_user_email_changed,
    log_backoffice_user_updated,
)
from apps.backoffice.services.users.update.apply import (
    apply_backoffice_user_regular_fields,
    get_backoffice_user_update_fields,
)
from apps.backoffice.services.users.update.email import (
    apply_backoffice_user_email_change,
    schedule_backoffice_email_verification_if_needed,
)
from apps.backoffice.services.users.update.payloads import (
    normalize_backoffice_user_update_data,
)
from apps.backoffice.services.users.update.save import save_backoffice_user_update
from apps.backoffice.services.users.update.validation import (
    validate_backoffice_user_update_common_rules,
)
from apps.users.models import User
from django.db import transaction


@transaction.atomic
def update_backoffice_user(
    *,
    actor,
    target_user: User,
    data: dict[str, Any],
    expected_updated_at=None,
    reason: str = "",
    request=None,
) -> User:
    """
    Обновляет пользователя из backoffice.

    Сервис отвечает только за редактирование базовых данных пользователя.
    Статусы, роли, блокировка, архивирование и удаление меняются отдельными
    сервисами.
    """

    locked_user = User.objects.select_for_update().get(id=target_user.id)

    validate_backoffice_user_update_common_rules(
        actor=actor,
        target_user=locked_user,
        expected_updated_at=expected_updated_at,
    )

    normalized_data = normalize_backoffice_user_update_data(data=data)

    email_changed, old_email, new_email = apply_backoffice_user_email_change(
        target_user=locked_user,
        new_email=normalized_data.get("email"),
    )
    changed_fields = apply_backoffice_user_regular_fields(
        target_user=locked_user,
        data=normalized_data,
    )

    update_fields = get_backoffice_user_update_fields(
        changed_fields=changed_fields,
        email_changed=email_changed,
    )

    save_backoffice_user_update(
        target_user=locked_user,
        update_fields=update_fields,
    )

    if changed_fields:
        log_backoffice_user_updated(
            actor=actor,
            target_user=locked_user,
            changed_fields=changed_fields,
            reason=reason,
            request=request,
        )

    if email_changed:
        log_backoffice_user_email_changed(
            actor=actor,
            target_user=locked_user,
            old_email=old_email,
            new_email=new_email,
            reason=reason,
            request=request,
        )

    schedule_backoffice_email_verification_if_needed(
        target_user=locked_user,
        email_changed=email_changed,
    )

    return locked_user


# Совместимый alias на время переноса старой admin-user логики.
admin_update_user = update_backoffice_user
