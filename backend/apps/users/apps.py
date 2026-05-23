from __future__ import annotations

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Конфигурация приложения users.

    Приложение users отвечает за пользователей, роли, профили,
    регистрацию, заявки, настройки, аудит и жизненный цикл аккаунтов.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
    label = "users"
    verbose_name = "Пользователи"
