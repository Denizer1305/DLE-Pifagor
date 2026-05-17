from __future__ import annotations

from apps.users.constants.lifecycle import UserStatus
from django.contrib.auth import get_user_model
from django.db.models import QuerySet

User = get_user_model()


def get_users_queryset() -> QuerySet:
    """
    Возвращает базовый QuerySet пользователей.

    Используется как единая точка входа для выборок пользователей.

    Returns:
        QuerySet: QuerySet модели User.
    """

    return User.objects.all()


def get_active_users_queryset() -> QuerySet:
    """
    Возвращает активных пользователей.

    Returns:
        QuerySet: Активные пользователи.
    """

    return get_users_queryset().filter(
        status=UserStatus.ACTIVE,
        is_active=True,
    )


def get_user_by_id(user_id: int):
    """
    Возвращает пользователя по ID.

    Args:
        user_id:
            ID пользователя.

    Returns:
        User | None: Пользователь или None.
    """

    if not user_id:
        return None

    return get_users_queryset().filter(id=user_id).first()


def get_user_by_email(email: str):
    """
    Возвращает пользователя по email.

    Args:
        email:
            Email пользователя.

    Returns:
        User | None: Пользователь или None.
    """

    if not email:
        return None

    return (
        get_users_queryset()
        .filter(
            email=email.strip().lower(),
        )
        .first()
    )


def get_user_by_phone(phone: str):
    """
    Возвращает пользователя по телефону.

    Args:
        phone:
            Телефон пользователя.

    Returns:
        User | None: Пользователь или None.
    """

    if not phone:
        return None

    return (
        get_users_queryset()
        .filter(
            phone=phone.strip(),
        )
        .first()
    )


def get_users_pending_email_queryset() -> QuerySet:
    """
    Возвращает пользователей, ожидающих подтверждения email.

    Returns:
        QuerySet: Пользователи со статусом pending_email.
    """

    return get_users_queryset().filter(status=UserStatus.PENDING_EMAIL)


def get_users_pending_review_queryset() -> QuerySet:
    """
    Возвращает пользователей, ожидающих проверки.

    Returns:
        QuerySet: Пользователи со статусом pending_review.
    """

    return get_users_queryset().filter(status=UserStatus.PENDING_REVIEW)


def get_blocked_users_queryset() -> QuerySet:
    """
    Возвращает заблокированных пользователей.

    Returns:
        QuerySet: Заблокированные пользователи.
    """

    return get_users_queryset().filter(status=UserStatus.BLOCKED)


def get_users_scheduled_for_deletion_queryset() -> QuerySet:
    """
    Возвращает пользователей, запланированных к удалению или анонимизации.

    Returns:
        QuerySet: Пользователи со статусом scheduled_for_deletion.
    """

    return get_users_queryset().filter(status=UserStatus.SCHEDULED_FOR_DELETION)


def get_managed_accounts_for_guardian(guardian) -> QuerySet:
    """
    Возвращает аккаунты, которыми управляет родитель или законный представитель.

    Обычно используется для детей младше 14 лет.

    Args:
        guardian:
            Родитель или законный представитель.

    Returns:
        QuerySet: Управляемые аккаунты.
    """

    if not guardian:
        return User.objects.none()

    return get_users_queryset().filter(account_managed_by=guardian)


def user_email_exists(email: str) -> bool:
    """
    Проверяет, существует ли пользователь с указанным email.

    Args:
        email:
            Email пользователя.

    Returns:
        bool: True, если email уже используется.
    """

    if not email:
        return False

    return (
        get_users_queryset()
        .filter(
            email=email.strip().lower(),
        )
        .exists()
    )


def user_phone_exists(phone: str) -> bool:
    """
    Проверяет, существует ли пользователь с указанным телефоном.

    Args:
        phone:
            Телефон пользователя.

    Returns:
        bool: True, если телефон уже используется.
    """

    if not phone:
        return False

    return (
        get_users_queryset()
        .filter(
            phone=phone.strip(),
        )
        .exists()
    )
