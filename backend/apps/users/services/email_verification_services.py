from __future__ import annotations

from apps.core.exceptions import ValidationApplicationError
from apps.users.selectors.user_selectors import get_user_by_id
from apps.users.services.audit_services import log_email_verified
from django.conf import settings
from django.core import signing
from django.db import transaction
from django.utils.http import urlencode

EMAIL_VERIFICATION_SALT = "users.email_verification"
EMAIL_VERIFICATION_MAX_AGE_SECONDS = 60 * 60 * 24


def create_email_verification_token(*, user) -> str:
    """
    Создаёт подписанный токен подтверждения email.

    Args:
        user:
            Пользователь, для которого создаётся токен.

    Returns:
        str: Подписанный токен подтверждения email.
    """

    return signing.dumps(
        {
            "user_id": user.id,
            "email": user.email,
        },
        salt=EMAIL_VERIFICATION_SALT,
    )


@transaction.atomic
def verify_email_token(*, token: str, request=None):
    """
    Проверяет токен подтверждения email и активирует email пользователя.

    Args:
        token:
            Подписанный токен.
        request:
            HTTP-запрос.

    Returns:
        User: Пользователь с подтверждённым email.

    Raises:
        ValidationApplicationError: Если токен недействителен.
    """

    try:
        payload = signing.loads(
            token,
            salt=EMAIL_VERIFICATION_SALT,
            max_age=EMAIL_VERIFICATION_MAX_AGE_SECONDS,
        )
    except signing.BadSignature as exc:
        raise ValidationApplicationError(
            "Ссылка подтверждения email недействительна или истекла.",
            code="invalid_email_verification_token",
        ) from exc

    user = get_user_by_id(payload.get("user_id"))

    if user is None:
        raise ValidationApplicationError(
            "Пользователь не найден.",
            code="user_not_found",
        )

    if user.email != payload.get("email"):
        raise ValidationApplicationError(
            "Email пользователя изменился. Запросите новую ссылку подтверждения.",
            code="email_changed",
        )

    user.mark_email_verified(save=True)

    log_email_verified(user=user, request=request)

    return user


def build_email_verification_url(*, user, frontend_base_url: str | None = None) -> str:
    """
    Формирует абсолютную ссылку подтверждения email.

    Args:
        user:
            Пользователь, которому отправляется письмо.
        frontend_base_url:
            Базовый URL frontend. Если не передан, берётся из настроек.

    Returns:
        str: Абсолютная ссылка на страницу подтверждения email.
    """

    token = create_email_verification_token(user=user)

    base_url = frontend_base_url or settings.FRONTEND_BASE_URL
    verify_path = getattr(settings, "EMAIL_VERIFY_PATH", "/auth/verify-email")

    return f"{base_url.rstrip('/')}{verify_path}?{urlencode({'token': token})}"
