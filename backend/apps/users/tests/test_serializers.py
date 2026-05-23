from __future__ import annotations

import pytest
from apps.users.serializers import (
    GuardianRegistrationSerializer,
    LearnerRegistrationSerializer,
    LoginSerializer,
    UserDetailSerializer,
    UserShortSerializer,
)
from apps.users.tests.factories import make_user


@pytest.mark.django_db
def test_user_short_serializer() -> None:
    """
    Проверяет краткий serializer пользователя.
    """

    user = make_user(
        email="short-serializer@example.com",
        first_name="Иван",
        last_name="Иванов",
    )

    data = UserShortSerializer(user).data

    assert data["id"] == user.id
    assert data["email"] == "short-serializer@example.com"
    assert data["full_name"] == "Иванов Иван"


@pytest.mark.django_db
def test_user_detail_serializer() -> None:
    """
    Проверяет детальный serializer пользователя.
    """

    user = make_user(email="detail-serializer@example.com")

    data = UserDetailSerializer(user).data

    assert data["id"] == user.id
    assert data["email"] == "detail-serializer@example.com"
    assert "status" in data
    assert "is_superuser" in data
    assert "created_at" in data


def test_login_serializer_valid_data() -> None:
    """
    Проверяет serializer входа.
    """

    serializer = LoginSerializer(
        data={
            "email": "login@example.com",
            "password": "StrongPassword123",
        }
    )

    assert serializer.is_valid() is True


@pytest.mark.django_db
def test_learner_registration_serializer_rejects_minor_self_registration() -> None:
    """
    Проверяет, что ребёнок младше 14 лет не может регистрироваться самостоятельно.
    """

    serializer = LearnerRegistrationSerializer(
        data={
            "email": "minor@example.com",
            "phone": "+79007772001",
            "password": "StrongPassword123",
            "first_name": "Пётр",
            "last_name": "Петров",
            "birth_date": "2020-01-01",
        }
    )

    assert serializer.is_valid() is False
    assert "non_field_errors" in serializer.errors


@pytest.mark.django_db
def test_guardian_registration_serializer_valid_data() -> None:
    """
    Проверяет serializer регистрации родителя.
    """

    serializer = GuardianRegistrationSerializer(
        data={
            "email": "guardian-serializer@example.com",
            "phone": "+79007772002",
            "password": "StrongPassword123",
            "first_name": "Мария",
            "last_name": "Петрова",
            "birth_date": "1985-01-01",
        }
    )

    assert serializer.is_valid() is True
