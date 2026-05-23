from __future__ import annotations

from collections.abc import Callable
from typing import Any

from apps.users.selectors.user_selectors import get_user_by_id


def send_user_email_or_retry(
    task,
    *,
    user_id: int,
    email_sender: Callable[..., int],
    user_kwarg: str = "user",
    skip_if_email_verified: bool = False,
    **email_kwargs: Any,
) -> bool:
    """
    Получает пользователя и отправляет письмо с поддержкой retry Celery.

    Args:
        task:
            Celery task instance.
        user_id:
            ID пользователя.
        email_sender:
            Функция отправки письма.
        user_kwarg:
            Имя аргумента, в который будет передан пользователь.
            Например: user или reviewer.
        skip_if_email_verified:
            Нужно ли пропустить отправку, если email уже подтверждён.
        **email_kwargs:
            Дополнительные аргументы для функции отправки письма.

    Returns:
        bool: True, если письмо отправлено или отправка не требуется.
        False, если пользователь не найден.
    """

    user = get_user_by_id(user_id)

    if user is None:
        return False

    if skip_if_email_verified and user.is_email_verified:
        return True

    try:
        email_sender(
            **{
                user_kwarg: user,
                **email_kwargs,
            }
        )
    except Exception as exc:
        raise task.retry(exc=exc) from exc

    return True
