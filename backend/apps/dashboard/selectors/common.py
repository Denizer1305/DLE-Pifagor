from __future__ import annotations

from django.apps import apps
from django.core.exceptions import FieldDoesNotExist


def get_optional_model(app_label: str, model_name: str):
    """
    Безопасно возвращает модель, если приложение уже подключено.

    Это позволяет dashboard не падать, если часть модулей ещё не готова
    или временно не подключена в INSTALLED_APPS.
    """

    try:
        return apps.get_model(app_label, model_name)
    except LookupError:
        return None


def model_has_field(model, field_name: str) -> bool:
    """
    Проверяет наличие поля у Django-модели.

    Args:
        model:
            Django model class.
        field_name:
            Имя поля.

    Returns:
        bool: True, если поле существует.
    """

    try:
        model._meta.get_field(field_name)
    except FieldDoesNotExist:
        return False

    return True
