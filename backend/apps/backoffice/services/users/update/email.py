from __future__ import annotations

from apps.users.constants.lifecycle import UserStatus
from apps.users.models import User
from apps.users.tasks.email_tasks import send_email_verification_task
from django.db import transaction


def apply_backoffice_user_email_change(
    *,
    target_user: User,
    new_email: str | None,
) -> tuple[bool, str, str]:
    """
    Применяет изменение email пользователя.

    После изменения email пользователь снова должен подтвердить почту.
    """

    if new_email is None:
        return False, "", ""

    normalized_new_email = new_email.strip().lower()
    old_email = target_user.email

    if old_email == normalized_new_email:
        return False, old_email, normalized_new_email

    target_user.email = normalized_new_email
    target_user.is_email_verified = False
    target_user.email_verified_at = None
    target_user.status = UserStatus.PENDING_EMAIL
    target_user.is_active = True

    return True, old_email, normalized_new_email


def schedule_backoffice_email_verification_if_needed(
    *,
    target_user: User,
    email_changed: bool,
) -> None:
    """
    Планирует отправку письма подтверждения email после commit.
    """

    if not email_changed:
        return

    transaction.on_commit(
        lambda: send_email_verification_task.delay(user_id=target_user.id)
    )


# Совместимые alias'ы на время переноса старой admin-user логики.
apply_admin_user_email_change = apply_backoffice_user_email_change
schedule_admin_email_verification_if_needed = (
    schedule_backoffice_email_verification_if_needed
)
