from __future__ import annotations

from apps.core.exceptions import ValidationApplicationError
from apps.users.selectors.user_selectors import get_user_by_email, get_user_by_id
from django.conf import settings
from django.core import signing
from django.db import transaction

PASSWORD_RESET_SALT = "users.password_reset"
PASSWORD_RESET_MAX_AGE_SECONDS = 60 * 60


def create_password_reset_token(*, user) -> str:
    """
    Создаёт токен восстановления пароля.

    Args:
        user:
            Пользователь.

    Returns:
        str: Подписанный токен восстановления пароля.
    """

    return signing.dumps(
        {
            "user_id": user.id,
            "email": user.email,
            "password": user.password,
        },
        salt=PASSWORD_RESET_SALT,
    )


def build_password_reset_url(*, user, frontend_base_url: str | None = None) -> str:
    """
    Формирует ссылку восстановления пароля.

    Args:
        user:
            Пользователь.
        frontend_base_url:
            Базовый URL frontend.

    Returns:
        str: Абсолютная ссылка восстановления.
    """

    token = create_password_reset_token(user=user)
    base_url = frontend_base_url or getattr(
        settings,
        "FRONTEND_BASE_URL",
        "http://localhost:5173",
    )

    return f"{base_url.rstrip('/')}/reset-password?token={token}"


def request_password_reset(*, email: str) -> bool:
    """
    Создаёт запрос восстановления пароля.

    В целях безопасности метод всегда возвращает True,
    даже если пользователь не найден. Так мы не раскрываем,
    зарегистрирован ли email на платформе.

    Args:
        email:
            Email пользователя.

    Returns:
        bool: True.
    """

    from apps.users.tasks import send_password_reset_task

    user = get_user_by_email(email)

    if user is None:
        return True

    if not user.is_active:
        return True

    send_password_reset_task.delay(user_id=user.id)

    return True


@transaction.atomic
def reset_password_by_token(*, token: str, password: str):
    """
    Устанавливает новый пароль по токену восстановления.

    Args:
        token:
            Подписанный токен восстановления.
        password:
            Новый пароль.

    Returns:
        User: Пользователь.

    Raises:
        ValidationApplicationError: Если токен недействителен.
    """

    try:
        payload = signing.loads(
            token,
            salt=PASSWORD_RESET_SALT,
            max_age=PASSWORD_RESET_MAX_AGE_SECONDS,
        )
    except signing.BadSignature as exc:
        raise ValidationApplicationError(
            "Ссылка восстановления пароля недействительна или истекла.",
            code="invalid_password_reset_token",
        ) from exc

    user = get_user_by_id(payload.get("user_id"))

    if user is None:
        raise ValidationApplicationError(
            "Пользователь не найден.",
            code="user_not_found",
        )

    if user.email != payload.get("email"):
        raise ValidationApplicationError(
            "Email пользователя изменился. Запросите новую ссылку восстановления.",
            code="email_changed",
        )

    if user.password != payload.get("password"):
        raise ValidationApplicationError(
            "Ссылка восстановления уже была использована. Запросите новую ссылку.",
            code="password_already_changed",
        )

    user.set_password(password)
    user.save(
        update_fields=[
            "password",
            "updated_at",
        ]
    )

    from apps.users.tasks.email_tasks import send_password_changed_task

    transaction.on_commit(
        lambda: send_password_changed_task.delay(user_id=user.id),
    )

    return user
