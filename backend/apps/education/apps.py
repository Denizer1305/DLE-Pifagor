from __future__ import annotations

from django.apps import AppConfig


class EducationConfig(AppConfig):
    """
    Конфигурация приложения education.

    Приложение education отвечает за академический слой платформы.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.education"
    label = "education"
    verbose_name = "Образовательная структура"
