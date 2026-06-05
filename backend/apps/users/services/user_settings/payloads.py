"""
Сборка payload для API пользовательских настроек.
"""

from __future__ import annotations

from copy import deepcopy

from apps.users.constants.settings import InterfaceLanguage
from apps.users.services.user_settings.defaults import (
    get_default_appearance_settings,
    get_default_notification_settings,
    get_default_privacy_settings,
    get_default_role_settings,
    get_default_security_settings,
)


def merge_settings(defaults: dict, current: dict | None) -> dict:
    """
    Рекурсивно объединяет дефолтные настройки с сохранёнными настройками.

    Сохранённые значения имеют приоритет, но если в БД нет новых ключей,
    они автоматически добавляются из дефолтной структуры.
    """

    result = deepcopy(defaults)

    if not isinstance(current, dict):
        return result

    for key, value in current.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_settings(result[key], value)
        else:
            result[key] = value

    return result


def build_settings_payload(*, settings_obj) -> dict:
    """
    Собирает полный payload пользовательских настроек.
    """

    return {
        "appearance": build_appearance_settings_payload(settings_obj=settings_obj),
        "notifications": build_notification_settings_payload(settings_obj=settings_obj),
        "privacy": build_privacy_settings_payload(settings_obj=settings_obj),
        "security": build_security_settings_payload(settings_obj=settings_obj),
        "roles": build_role_settings_payload(settings_obj=settings_obj),
    }


def build_appearance_settings_payload(*, settings_obj) -> dict:
    """
    Собирает настройки внешнего вида с учётом дефолтов.
    """

    payload = merge_settings(
        get_default_appearance_settings(),
        settings_obj.appearance_settings,
    )
    payload["language"] = settings_obj.language or InterfaceLanguage.RUSSIAN

    return payload


def build_notification_settings_payload(*, settings_obj) -> dict:
    """
    Собирает настройки уведомлений с учётом дефолтов.
    """

    return merge_settings(
        get_default_notification_settings(),
        settings_obj.notification_settings,
    )


def build_privacy_settings_payload(*, settings_obj) -> dict:
    """
    Собирает настройки приватности с учётом дефолтов.
    """

    return merge_settings(
        get_default_privacy_settings(),
        settings_obj.privacy_settings,
    )


def build_security_settings_payload(*, settings_obj) -> dict:
    """
    Собирает настройки безопасности с учётом дефолтов.
    """

    return merge_settings(
        get_default_security_settings(),
        settings_obj.security_settings,
    )


def build_role_settings_payload(*, settings_obj) -> dict:
    """
    Собирает ролевые настройки с учётом дефолтов.
    """

    return merge_settings(
        get_default_role_settings(),
        settings_obj.role_settings,
    )
