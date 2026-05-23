from __future__ import annotations

import pytest
from apps.users.constants.lifecycle import UserStatus
from apps.users.services.user_lifecycle_services import (
    activate_user,
    anonymize_user,
    block_user,
    schedule_user_deletion,
)
from apps.users.tests.factories import make_user


@pytest.mark.django_db
def test_activate_user() -> None:
    """
    Проверяет активацию пользователя.
    """

    user = make_user(
        email="activate@example.com",
        status=UserStatus.PENDING_REVIEW,
        is_active=False,
    )

    activate_user(user=user)

    user.refresh_from_db()

    assert user.status == UserStatus.ACTIVE
    assert user.is_active is True


@pytest.mark.django_db
def test_block_user() -> None:
    """
    Проверяет блокировку пользователя.
    """

    user = make_user(email="block@example.com")

    block_user(user=user, reason="Тестовая блокировка.")

    user.refresh_from_db()

    assert user.status == UserStatus.BLOCKED
    assert user.is_active is False


@pytest.mark.django_db
def test_schedule_user_deletion() -> None:
    """
    Проверяет планирование удаления пользователя.
    """

    user = make_user(email="schedule-delete@example.com")

    schedule_user_deletion(
        user=user,
        reason="Тестовое удаление.",
    )

    user.refresh_from_db()

    assert user.status == UserStatus.SCHEDULED_FOR_DELETION
    assert user.is_active is False
    assert user.scheduled_for_deletion_at is not None


@pytest.mark.django_db
def test_anonymize_user() -> None:
    """
    Проверяет анонимизацию пользователя.
    """

    user = make_user(
        email="anonymize@example.com",
        phone="+79007770010",
        first_name="Иван",
        last_name="Иванов",
    )

    anonymize_user(
        user=user,
        reason="Тестовая анонимизация.",
    )

    user.refresh_from_db()

    assert user.status == UserStatus.ANONYMIZED
    assert user.is_active is False
    assert user.is_login_allowed is False
    assert user.email.startswith("anon-")
    assert user.email.endswith("@pifagor.local")
    assert user.first_name == "Анонимизирован"
    assert user.last_name == "Пользователь"
    assert user.has_usable_password() is False
