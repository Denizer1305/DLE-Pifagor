from __future__ import annotations

from django.apps import AppConfig


class CourseConfig(AppConfig):
    """
    Конфигурация приложения курсов.

    Модуль отвечает за академические и авторские курсы,
    КТП, структуру уроков, доступы к курсам и прогресс обучения.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.course"
    verbose_name = "Курсы"
