from __future__ import annotations

from django.apps import AppConfig


class OrganizationsConfig(AppConfig):
    """
    Конфигурация приложения organizations.

    Приложение отвечает за образовательные организации,
    отделения и учебные группы.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.organizations"
    label = "organizations"
    verbose_name = "Образовательные организации"
