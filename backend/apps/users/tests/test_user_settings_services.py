from __future__ import annotations

import pytest
from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.constants.roles import RoleCode
from apps.users.models import UserRole, UserSettings
from apps.users.services import (
    create_default_user_settings,
    set_active_role,
    update_compact_mode,
    update_interface_theme,
    update_language,
    update_timezone,
)
from apps.users.tests.factories import make_role, make_user


@pytest.mark.django_db
def test_create_default_user_settings() -> None:
    """
    Проверяет создание настроек пользователя по умолчанию.
    """

    user = make_user(email="settings@example.com")

    settings = create_default_user_settings(user=user)

    assert settings.user == user
    assert settings.language == "ru"
    assert settings.timezone == "Europe/Moscow"
    assert settings.interface_theme == UserSettings.InterfaceTheme.DEFAULT


@pytest.mark.django_db
def test_update_interface_theme() -> None:
    """
    Проверяет обновление темы интерфейса.
    """

    user = make_user(email="theme@example.com")

    settings = update_interface_theme(
        user=user,
        interface_theme=UserSettings.InterfaceTheme.COLLEGE,
    )

    assert settings.interface_theme == UserSettings.InterfaceTheme.COLLEGE


@pytest.mark.django_db
def test_update_language() -> None:
    """
    Проверяет обновление языка интерфейса.
    """

    user = make_user(email="language@example.com")

    settings = update_language(user=user, language="ru")

    assert settings.language == "ru"


@pytest.mark.django_db
def test_update_timezone() -> None:
    """
    Проверяет обновление часового пояса.
    """

    user = make_user(email="timezone@example.com")

    settings = update_timezone(user=user, timezone="Europe/Moscow")

    assert settings.timezone == "Europe/Moscow"


@pytest.mark.django_db
def test_update_compact_mode() -> None:
    """
    Проверяет обновление компактного режима.
    """

    user = make_user(email="compact@example.com")

    settings = update_compact_mode(user=user, compact_mode=True)

    assert settings.compact_mode is True


@pytest.mark.django_db
def test_set_active_role() -> None:
    """
    Проверяет установку активной роли пользователя.
    """

    user = make_user(email="active-role@example.com")
    role = make_role(code=RoleCode.LEARNER)

    UserRole.objects.create(
        user=user,
        role=role,
        status=UserRoleStatus.ACTIVE,
    )

    settings = set_active_role(
        user=user,
        role_code=RoleCode.LEARNER,
    )

    assert settings.active_role == RoleCode.LEARNER
