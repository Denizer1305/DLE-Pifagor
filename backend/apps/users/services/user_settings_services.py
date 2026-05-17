from __future__ import annotations

from apps.core.exceptions import ValidationApplicationError
from apps.users.constants.roles import RoleCode
from apps.users.models import UserSettings
from apps.users.selectors.role_selectors import user_has_active_role


def create_default_user_settings(*, user) -> UserSettings:
    """
    Создаёт настройки пользователя по умолчанию.

    Args:
        user:
            Пользователь.

    Returns:
        UserSettings: Созданные или существующие настройки.
    """

    settings, _created = UserSettings.objects.get_or_create(
        user=user,
        defaults={
            "language": "ru",
            "timezone": "Europe/Moscow",
            "active_role": "",
            "interface_theme": UserSettings.InterfaceTheme.DEFAULT,
            "compact_mode": False,
        },
    )

    return settings


def set_active_role(*, user, role_code: str) -> UserSettings:
    """
    Устанавливает активную роль пользователя.

    Args:
        user:
            Пользователь.
        role_code:
            Код роли.

    Returns:
        UserSettings: Обновлённые настройки.

    Raises:
        ValidationApplicationError: Если роль недоступна пользователю.
    """

    if role_code not in RoleCode.values:
        raise ValidationApplicationError(
            "Недопустимая роль.",
            code="invalid_role",
        )

    if not user_has_active_role(user=user, role_code=role_code):
        raise ValidationApplicationError(
            "Пользователь не имеет такой активной роли.",
            code="role_not_available",
        )

    settings = create_default_user_settings(user=user)
    settings.active_role = role_code
    settings.save(update_fields=["active_role", "updated_at"])

    return settings


def update_interface_theme(*, user, interface_theme: str) -> UserSettings:
    """
    Обновляет тему интерфейса пользователя.

    Args:
        user:
            Пользователь.
        interface_theme:
            Код темы интерфейса.

    Returns:
        UserSettings: Обновлённые настройки.
    """

    if interface_theme not in UserSettings.InterfaceTheme.values:
        raise ValidationApplicationError(
            "Недопустимая тема интерфейса.",
            code="invalid_interface_theme",
        )

    settings = create_default_user_settings(user=user)
    settings.interface_theme = interface_theme
    settings.save(update_fields=["interface_theme", "updated_at"])

    return settings


def update_language(*, user, language: str) -> UserSettings:
    """
    Обновляет язык интерфейса пользователя.

    Args:
        user:
            Пользователь.
        language:
            Код языка.

    Returns:
        UserSettings: Обновлённые настройки.
    """

    if not language:
        raise ValidationApplicationError(
            "Язык интерфейса обязателен.",
            code="language_required",
        )

    settings = create_default_user_settings(user=user)
    settings.language = language
    settings.save(update_fields=["language", "updated_at"])

    return settings


def update_timezone(*, user, timezone: str) -> UserSettings:
    """
    Обновляет часовой пояс пользователя.

    Args:
        user:
            Пользователь.
        timezone:
            Часовой пояс.

    Returns:
        UserSettings: Обновлённые настройки.
    """

    if not timezone:
        raise ValidationApplicationError(
            "Часовой пояс обязателен.",
            code="timezone_required",
        )

    settings = create_default_user_settings(user=user)
    settings.timezone = timezone
    settings.save(update_fields=["timezone", "updated_at"])

    return settings


def update_compact_mode(*, user, compact_mode: bool) -> UserSettings:
    """
    Обновляет компактный режим интерфейса.

    Args:
        user:
            Пользователь.
        compact_mode:
            Включён ли компактный режим.

    Returns:
        UserSettings: Обновлённые настройки.
    """

    settings = create_default_user_settings(user=user)
    settings.compact_mode = compact_mode
    settings.save(update_fields=["compact_mode", "updated_at"])

    return settings
