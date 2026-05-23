from __future__ import annotations

import pytest
from apps.users.services.auth_services import create_token_pair_for_user
from apps.users.tests.factories import make_user
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_refresh_access_token_from_cookie(settings) -> None:
    """
    Проверяет обновление access token из refresh cookie.
    """

    client = APIClient()
    user = make_user(
        email="refresh-user@example.com",
        is_email_verified=True,
        is_login_allowed=True,
    )
    tokens = create_token_pair_for_user(user)

    client.cookies[settings.JWT_REFRESH_COOKIE_NAME] = tokens["refresh"]

    response = client.post("/api/v1/users/auth/refresh/", {})

    assert response.status_code == 200
    assert "access" in response.data
    assert response.data["access"]


@pytest.mark.django_db
def test_refresh_access_token_without_cookie_returns_401() -> None:
    """
    Проверяет ошибку обновления access token без refresh cookie.
    """

    client = APIClient()

    response = client.post("/api/v1/users/auth/refresh/", {})

    assert response.status_code == 401
