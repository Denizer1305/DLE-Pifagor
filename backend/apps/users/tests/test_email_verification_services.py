from __future__ import annotations

import pytest
from apps.users.constants.lifecycle import UserStatus
from apps.users.services.email_verification_services import (
    build_email_verification_url,
    create_email_verification_token,
    verify_email_token,
)
from apps.users.tests.factories import make_user


@pytest.mark.django_db
def test_create_email_verification_token() -> None:
    """
    Проверяет создание токена подтверждения email.
    """

    user = make_user(
        email="verify-token@example.com",
        is_email_verified=False,
        status=UserStatus.PENDING_EMAIL,
    )

    token = create_email_verification_token(user=user)

    assert isinstance(token, str)
    assert token


@pytest.mark.django_db
def test_verify_email_token_marks_email_verified() -> None:
    """
    Проверяет подтверждение email по токену.
    """

    user = make_user(
        email="verify-email@example.com",
        is_email_verified=False,
        status=UserStatus.PENDING_EMAIL,
    )
    token = create_email_verification_token(user=user)

    verified_user = verify_email_token(token=token)

    verified_user.refresh_from_db()

    assert verified_user.id == user.id
    assert verified_user.is_email_verified is True
    assert verified_user.email_verified_at is not None
    assert verified_user.status == UserStatus.PENDING_REVIEW


@pytest.mark.django_db
def test_build_email_verification_url() -> None:
    """
    Проверяет генерацию ссылки подтверждения email.
    """

    user = make_user(email="verify-url@example.com")

    url = build_email_verification_url(
        user=user,
        frontend_base_url="http://localhost:5173",
    )

    assert url.startswith("http://localhost:5173/auth/verify-email?token=")
