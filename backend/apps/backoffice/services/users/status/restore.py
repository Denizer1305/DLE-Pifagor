from __future__ import annotations

from apps.users.constants.lifecycle import UserStatus
from apps.users.models import User


def get_restored_user_status(*, target_user: User) -> str:
    """
    Определяет статус пользователя после восстановления.

    Если email не подтверждён, пользователь возвращается в ожидание
    подтверждения email. Если email подтверждён, пользователь становится активным.
    """

    if not target_user.is_email_verified:
        return UserStatus.PENDING_EMAIL

    return UserStatus.ACTIVE


def clear_user_archive_fields(*, target_user: User) -> list[str]:
    """
    Очищает архивные поля пользователя и возвращает изменённые поля.
    """

    changed_fields: list[str] = []

    if hasattr(target_user, "archived_at"):
        target_user.archived_at = None
        changed_fields.append("archived_at")

    if hasattr(target_user, "archived_by"):
        target_user.archived_by = None
        changed_fields.append("archived_by")

    if hasattr(target_user, "archive_reason"):
        target_user.archive_reason = ""
        changed_fields.append("archive_reason")

    return changed_fields
