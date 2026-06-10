from __future__ import annotations

from django.apps import AppConfig


class MaterialsConfig(AppConfig):
    """
    Конфигурация приложения учебных материалов.

    Модуль отвечает за библиотеку материалов платформы:
    файлы, ссылки, тексты, презентации, видео, версии материалов
    и журнал использования материалов в курсах и заданиях.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.materials"
    verbose_name = "Учебные материалы"
