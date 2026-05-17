from __future__ import annotations

from itertools import count

from apps.users.constants.lifecycle import UserStatus
from apps.users.constants.roles import ROLE_LABELS, ROLE_SORT_ORDER, RoleCode
from apps.users.models import Role, User

_user_counter = count(1)


def make_user(
    *,
    email: str | None = None,
    phone: str | None = None,
    password: str = "StrongPassword123",
    first_name: str = "Иван",
    last_name: str = "Иванов",
    middle_name: str = "",
    status: str = UserStatus.ACTIVE,
    is_active: bool = True,
    is_email_verified: bool = True,
    is_phone_verified: bool = False,
    is_login_allowed: bool = True,
    **extra_fields,
) -> User:
    """
    Создаёт пользователя для тестов.

    Args:
        email:
            Email пользователя.
        phone:
            Телефон пользователя.
        password:
            Пароль пользователя.
        first_name:
            Имя.
        last_name:
            Фамилия.
        middle_name:
            Отчество.
        status:
            Статус аккаунта.
        is_active:
            Активен ли пользователь.
        is_email_verified:
            Подтверждён ли email.
        is_phone_verified:
            Подтверждён ли телефон.
        is_login_allowed:
            Разрешён ли самостоятельный вход.
        **extra_fields:
            Дополнительные поля User.

    Returns:
        User: Созданный пользователь.
    """

    index = next(_user_counter)

    user = User.objects.create_user(
        email=email or f"user{index}@example.com",
        phone=phone or f"+7900000{index:04d}",
        password=password,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
        status=status,
        is_active=is_active,
        is_email_verified=is_email_verified,
        is_phone_verified=is_phone_verified,
        is_login_allowed=is_login_allowed,
        **extra_fields,
    )

    return user


def make_role(
    *,
    code: str = RoleCode.LEARNER,
    label: str | None = None,
    is_active: bool = True,
) -> Role:
    """
    Создаёт или обновляет роль для тестов.

    Args:
        code:
            Код роли.
        label:
            Название роли.
        is_active:
            Активна ли роль.

    Returns:
        Role: Созданная или обновлённая роль.
    """

    role, _created = Role.objects.update_or_create(
        code=code,
        defaults={
            "label": label or ROLE_LABELS.get(code, code),
            "is_system": True,
            "is_active": is_active,
            "sort_order": ROLE_SORT_ORDER.get(code, 100),
        },
    )

    return role


def make_system_roles() -> list[Role]:
    """
    Создаёт все системные роли для тестов.

    Returns:
        list[Role]: Список ролей.
    """

    return [make_role(code=role_code) for role_code, _label in RoleCode.choices]
