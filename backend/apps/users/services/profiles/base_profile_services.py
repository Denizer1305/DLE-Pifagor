from __future__ import annotations

from apps.users.models import Profile


def create_base_profile(*, user) -> Profile:
    """
    Создаёт базовый профиль пользователя.

    Args:
        user:
            Пользователь.

    Returns:
        Profile: Созданный или существующий базовый профиль.
    """

    profile, _created = Profile.objects.get_or_create(user=user)

    return profile
