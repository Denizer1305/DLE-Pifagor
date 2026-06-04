"""
Фабрики тестовых данных для приложения notifications.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model

User = get_user_model()


def create_test_user(
    *,
    email: str,
    password: str = "StrongPassword123!",
    phone: str = "+79000000000",
    first_name: str = "Тест",
    last_name: str = "Пользователь",
    **extra_fields,
):
    """
    Создаёт тестового пользователя с обязательными полями проекта.
    """

    return User.objects.create_user(
        email=email,
        phone=phone,
        password=password,
        first_name=first_name,
        last_name=last_name,
        **extra_fields,
    )
