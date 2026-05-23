from __future__ import annotations

from apps.users.constants.moderation import ModerationStatus
from apps.users.models import Profile
from django.db.models import QuerySet


def get_profiles_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet профилей пользователей.

    Returns:
        QuerySet: Профили пользователей.
    """

    return Profile.objects.select_related("user")


def get_profile_by_user(user):
    """
    Возвращает базовый профиль пользователя.

    Args:
        user:
            Пользователь.

    Returns:
        Profile | None: Профиль пользователя или None.
    """

    if not user:
        return None

    return get_profiles_queryset().filter(user=user).first()


def get_profiles_pending_avatar_moderation() -> QuerySet:
    """
    Возвращает профили, у которых аватар ожидает модерации.

    Returns:
        QuerySet: Профили с аватаром на модерации.
    """

    return get_profiles_queryset().filter(
        avatar_moderation_status=ModerationStatus.PENDING,
    )


def get_profiles_pending_profile_moderation() -> QuerySet:
    """
    Возвращает профили, публичные данные которых ожидают модерации.

    Returns:
        QuerySet: Профили на модерации.
    """

    return get_profiles_queryset().filter(
        profile_moderation_status=ModerationStatus.PENDING,
    )
