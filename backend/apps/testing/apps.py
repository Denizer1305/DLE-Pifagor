from __future__ import annotations

from django.apps import AppConfig


class TestingConfig(AppConfig):
    """
    Конфигурация приложения тестирования.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.testing"
    verbose_name = "Тестирование"
