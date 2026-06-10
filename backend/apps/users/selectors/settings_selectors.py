"""
Selectors для пользовательских настроек.
"""

from __future__ import annotations

from apps.users.models import UserSettings


def get_or_create_settings_for_user(user) -> UserSettings:
    """
    Возвращает или создаёт объект персональных настроек пользователя.
    """

    settings_obj, _created = UserSettings.objects.get_or_create(user=user)

    return settings_obj
