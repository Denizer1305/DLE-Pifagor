from __future__ import annotations

from apps.core.exceptions import ValidationApplicationError
from apps.users.constants.audit import UserAuditAction
from apps.users.constants.lifecycle import ProfileStatus
from apps.users.constants.moderation import ModerationStatus
from apps.users.models import Profile
from apps.users.services.audit_services import create_user_audit_log


def submit_avatar_for_moderation(*, profile: Profile) -> Profile:
    """
    Отправляет аватар профиля на модерацию.

    Args:
        profile:
            Базовый профиль пользователя.

    Returns:
        Profile: Обновлённый профиль.
    """

    profile.avatar_moderation_status = ModerationStatus.PENDING
    profile.save(update_fields=["avatar_moderation_status", "updated_at"])

    return profile


def moderate_avatar(
    *,
    profile: Profile,
    moderator,
    is_approved: bool,
    comment: str = "",
    request=None,
) -> Profile:
    """
    Модерирует аватар пользователя.

    Args:
        profile:
            Базовый профиль пользователя.
        moderator:
            Модератор.
        is_approved:
            Одобрен ли аватар.
        comment:
            Комментарий модератора.
        request:
            HTTP-запрос.

    Returns:
        Profile: Обновлённый профиль.
    """

    profile.avatar_moderation_status = (
        ModerationStatus.APPROVED if is_approved else ModerationStatus.REJECTED
    )
    profile.moderation_comment = comment or ""
    profile.save(
        update_fields=[
            "avatar_moderation_status",
            "moderation_comment",
            "updated_at",
        ]
    )

    create_user_audit_log(
        actor=moderator,
        target_user=profile.user,
        action=(
            UserAuditAction.AVATAR_APPROVED
            if is_approved
            else UserAuditAction.AVATAR_REJECTED
        ),
        message=(
            "Аватар пользователя одобрен."
            if is_approved
            else "Аватар пользователя отклонён."
        ),
        request=request,
    )

    return profile


def reject_profile(*, profile, rejected_by=None, comment: str = "", request=None):
    """
    Отклоняет ролевой профиль пользователя.

    Args:
        profile:
            Ролевой профиль.
        rejected_by:
            Пользователь, отклонивший профиль.
        comment:
            Комментарий.
        request:
            HTTP-запрос.

    Returns:
        object: Обновлённый профиль.
    """

    if not hasattr(profile, "status"):
        raise ValidationApplicationError(
            "Переданный объект не является проверяемым профилем.",
            code="invalid_profile",
        )

    profile.status = ProfileStatus.REJECTED

    if hasattr(profile, "verification_comment"):
        profile.verification_comment = comment or ""

    profile.save()

    create_user_audit_log(
        actor=rejected_by,
        target_user=profile.user,
        action=UserAuditAction.PROFILE_REJECTED,
        message="Профиль пользователя отклонён.",
        request=request,
    )

    return profile
