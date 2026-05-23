from __future__ import annotations

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Конфигурация приложения core.

    Приложение core содержит общие базовые классы, исключения,
    утилиты, пагинацию, permissions и инфраструктурные элементы проекта.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"
    label = "core"
    verbose_name = "Ядро проекта"
