from __future__ import annotations

from apps.users.validators.user_validators import validate_user_can_login
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken


def create_token_pair_for_user(user) -> dict:
    """
    Создаёт пару JWT-токенов для пользователя.

    Args:
        user:
            Пользователь.

    Returns:
        dict: access и refresh token.
    """

    refresh = RefreshToken.for_user(user)

    return {
        "access": str(refresh.access_token),
        "refresh": str(refresh),
    }


def authenticate_user(*, email: str, password: str):
    """
    Аутентифицирует пользователя по email и паролю.

    Args:
        email:
            Email пользователя.
        password:
            Пароль пользователя.

    Returns:
        User: Аутентифицированный пользователь.

    Raises:
        AuthenticationFailed: Если данные неверные или вход запрещён.
    """

    user = authenticate(
        username=email.lower().strip(),
        password=password,
    )

    if user is None:
        raise AuthenticationFailed("Неверный email или пароль.")

    validate_user_can_login(user)

    return user


def login_user(*, email: str, password: str, request=None) -> dict:
    """
    Выполняет вход пользователя и создаёт JWT-токены.

    Args:
        email:
            Email пользователя.
        password:
            Пароль пользователя.
        request:
            HTTP-запрос.

    Returns:
        dict: user, access и refresh.
    """

    user = authenticate_user(
        email=email,
        password=password,
    )

    tokens = create_token_pair_for_user(user)

    return {
        "user": user,
        "access": tokens["access"],
        "refresh": tokens["refresh"],
    }


def get_refresh_token_from_request(request) -> str:
    """
    Получает refresh token из cookie или тела запроса.

    Args:
        request:
            DRF request.

    Returns:
        str: Refresh token.

    Raises:
        AuthenticationFailed: Если refresh token отсутствует.
    """

    cookie_name = settings.JWT_REFRESH_COOKIE_NAME

    refresh_token = request.COOKIES.get(cookie_name)

    if not refresh_token:
        refresh_token = request.data.get("refresh", "")

    if not refresh_token:
        raise AuthenticationFailed("Refresh token отсутствует.")

    return refresh_token


def refresh_access_token(*, request) -> dict:
    """
    Обновляет access token по refresh token.

    Refresh token берётся из httpOnly cookie или тела запроса.

    Args:
        request:
            DRF request.

    Returns:
        dict: Новый access token.

    Raises:
        AuthenticationFailed: Если refresh token недействителен.
    """

    refresh_token = get_refresh_token_from_request(request)

    try:
        refresh = RefreshToken(refresh_token)
        access = refresh.access_token
    except TokenError as exc:
        raise AuthenticationFailed("Refresh token недействителен или истёк.") from exc

    return {
        "access": str(access),
    }


def set_refresh_token_cookie(*, response, refresh_token: str):
    """
    Устанавливает refresh token в httpOnly cookie.

    Args:
        response:
            DRF Response.
        refresh_token:
            Refresh token.

    Returns:
        Response: Ответ с установленной cookie.
    """

    response.set_cookie(
        key=settings.JWT_REFRESH_COOKIE_NAME,
        value=refresh_token,
        httponly=settings.JWT_REFRESH_COOKIE_HTTP_ONLY,
        secure=settings.JWT_REFRESH_COOKIE_SECURE,
        samesite=settings.JWT_REFRESH_COOKIE_SAMESITE,
        path=settings.JWT_REFRESH_COOKIE_PATH,
        max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
    )

    return response


def clear_refresh_token_cookie(*, response):
    """
    Удаляет refresh token cookie.

    Args:
        response:
            DRF Response.

    Returns:
        Response: Ответ с удалённой cookie.
    """

    response.delete_cookie(
        key=settings.JWT_REFRESH_COOKIE_NAME,
        path=settings.JWT_REFRESH_COOKIE_PATH,
        samesite=settings.JWT_REFRESH_COOKIE_SAMESITE,
    )

    return response


def blacklist_refresh_token(refresh_token: str) -> None:
    """
    Добавляет refresh token в blacklist, если blacklist подключён.

    Args:
        refresh_token:
            Refresh token.
    """

    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except AttributeError:
        return
    except TokenError:
        return
