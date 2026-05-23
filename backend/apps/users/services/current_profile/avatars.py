from __future__ import annotations

from apps.users.constants.audit import UserAuditAction
from apps.users.selectors.current_profile_selectors import (
    get_or_create_profile_for_user,
)
from apps.users.services.audit_services import create_user_audit_log
from apps.users.services.current_profile.payloads import build_current_profile_payload
from django.db import transaction


@transaction.atomic
def update_current_profile_avatar(*, user, avatar, request=None) -> dict:
    """
    Обновляет аватар текущего пользователя.
    """

    profile = get_or_create_profile_for_user(user)
    profile.avatar = avatar
    profile.submit_avatar_for_moderation(save=False)
    profile.full_clean()
    profile.save(
        update_fields=[
            "avatar",
            "avatar_moderation_status",
            "updated_at",
        ],
    )

    create_user_audit_log(
        actor=user,
        target_user=user,
        action=UserAuditAction.PROFILE_UPDATED,
        message="Пользователь обновил аватар профиля.",
        request=request,
    )

    return build_current_profile_payload(user=user)


@transaction.atomic
def delete_current_profile_avatar(*, user, request=None) -> dict:
    """
    Удаляет аватар текущего пользователя.
    """

    profile = get_or_create_profile_for_user(user)

    if profile.avatar:
        profile.avatar.delete(save=False)

    profile.avatar = None
    profile.save(update_fields=["avatar", "updated_at"])

    create_user_audit_log(
        actor=user,
        target_user=user,
        action=UserAuditAction.PROFILE_UPDATED,
        message="Пользователь удалил аватар профиля.",
        request=request,
    )

    return build_current_profile_payload(user=user)
