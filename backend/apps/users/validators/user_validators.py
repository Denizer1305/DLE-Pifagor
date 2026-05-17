from __future__ import annotations

from apps.users.selectors.user_selectors import user_email_exists, user_phone_exists
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_unique_email(email: str, *, exclude_user=None) -> None:
    """
    Проверяет уникальность email пользователя.

    Args:
        email:
            Email пользователя.
        exclude_user:
            Пользователь, которого нужно исключить из проверки.
            Используется при обновлении собственного email.

    Raises:
        ValidationError: Если email уже используется.
    """

    if not email:
        raise ValidationError(_("Email обязателен."))

    normalized_email = email.strip().lower()

    queryset_exists = user_email_exists(normalized_email)

    if not queryset_exists:
        return

    if exclude_user and exclude_user.email == normalized_email:
        return

    raise ValidationError(_("Пользователь с таким email уже существует."))


def validate_unique_phone(phone: str, *, exclude_user=None) -> None:
    """
    Проверяет уникальность телефона пользователя.

    Args:
        phone:
            Телефон пользователя.
        exclude_user:
            Пользователь, которого нужно исключить из проверки.
            Используется при обновлении собственного телефона.

    Raises:
        ValidationError: Если телефон уже используется.
    """

    if not phone:
        raise ValidationError(_("Телефон обязателен."))

    normalized_phone = phone.strip()

    queryset_exists = user_phone_exists(normalized_phone)

    if not queryset_exists:
        return

    if exclude_user and exclude_user.phone == normalized_phone:
        return

    raise ValidationError(_("Пользователь с таким телефоном уже существует."))


def validate_user_can_login(user) -> None:
    """
    Проверяет, может ли пользователь выполнить самостоятельный вход.

    Args:
        user:
            Пользователь.

    Raises:
        ValidationError: Если вход запрещён.
    """

    if not user.is_active:
        raise ValidationError(_("Аккаунт неактивен или заблокирован."))

    if not user.is_login_allowed:
        raise ValidationError(_("Самостоятельный вход в этот аккаунт пока недоступен."))

    if not user.is_email_verified:
        raise ValidationError(_("Email пользователя не подтверждён."))


def validate_user_is_not_anonymized(user) -> None:
    """
    Проверяет, что пользователь не анонимизирован.

    Args:
        user:
            Пользователь.

    Raises:
        ValidationError: Если пользователь анонимизирован.
    """

    if getattr(user, "is_anonymized", False):
        raise ValidationError(_("Аккаунт пользователя анонимизирован."))
