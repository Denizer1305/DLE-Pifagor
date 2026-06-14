from __future__ import annotations

from django.apps import AppConfig


class BackofficeConfig(AppConfig):
    """
    Конфигурация административного backend-приложения.

    Backoffice содержит сценарии управления платформой:
    пользователи, роли, статусы, аудит, bulk-операции.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.backoffice"
    verbose_name = "Административный контур"
