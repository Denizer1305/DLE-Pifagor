from __future__ import annotations

from django.contrib.auth import get_user_model

User = get_user_model()


def create_test_user(
    *,
    email: str,
    phone: str,
    password: str = "StrongPassword123!",
    first_name: str = "",
    last_name: str = "",
    middle_name: str = "",
):
    """
    Создаёт пользователя для тестов organizations.

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

    Returns:
        User: Созданный пользователь.
    """

    return User.objects.create_user(
        email=email,
        phone=phone,
        password=password,
        first_name=first_name,
        last_name=last_name,
        middle_name=middle_name,
    )
