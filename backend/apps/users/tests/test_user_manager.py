from __future__ import annotations

import pytest
from apps.users.constants.lifecycle import UserStatus
from apps.users.models import User


@pytest.mark.django_db
def test_create_user_with_email_as_login() -> None:
    """
    Проверяет создание обычного пользователя через UserManager.
    """

    user = User.objects.create_user(
        email="TestUser@Example.COM",
        phone="+79001112233",
        password="StrongPassword123",
        first_name="Иван",
        last_name="Иванов",
    )

    assert user.email == "testuser@example.com"
    assert user.phone == "+79001112233"
    assert user.check_password("StrongPassword123")
    assert user.status == UserStatus.PENDING_EMAIL
    assert user.is_active is True
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_create_user_requires_email() -> None:
    """
    Проверяет, что email обязателен при создании пользователя.
    """

    with pytest.raises(ValueError):
        User.objects.create_user(
            email="",
            phone="+79001112233",
            password="StrongPassword123",
            first_name="Иван",
            last_name="Иванов",
        )


@pytest.mark.django_db
def test_create_user_requires_phone() -> None:
    """
    Проверяет, что телефон обязателен при создании пользователя.
    """

    with pytest.raises(ValueError):
        User.objects.create_user(
            email="user@example.com",
            phone="",
            password="StrongPassword123",
            first_name="Иван",
            last_name="Иванов",
        )


@pytest.mark.django_db
def test_create_superuser_sets_required_flags() -> None:
    """
    Проверяет создание суперпользователя.
    """

    user = User.objects.create_superuser(
        email="admin@example.com",
        phone="+79001112234",
        password="StrongPassword123",
        first_name="Админ",
        last_name="Платформы",
    )

    assert user.is_staff is True
    assert user.is_superuser is True
    assert user.is_email_verified is True
    assert user.is_phone_verified is True
    assert user.status == UserStatus.ACTIVE


@pytest.mark.django_db
def test_create_managed_child_user_disables_login() -> None:
    """
    Проверяет создание управляемого аккаунта ребёнка.
    """

    guardian = User.objects.create_user(
        email="guardian@example.com",
        phone="+79001112235",
        password="StrongPassword123",
        first_name="Мария",
        last_name="Петрова",
    )

    child = User.objects.create_managed_child_user(
        email="child@example.com",
        phone="+79001112236",
        password="StrongPassword123",
        first_name="Пётр",
        last_name="Петров",
        account_managed_by=guardian,
    )

    assert child.account_managed_by == guardian
    assert child.is_login_allowed is False
    assert child.status == UserStatus.PENDING_REVIEW
