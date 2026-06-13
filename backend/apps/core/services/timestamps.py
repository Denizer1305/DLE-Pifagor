from __future__ import annotations

from django.db import models
from django.utils import timezone


def set_now(instance: models.Model, field_name: str) -> None:
    """
    Устанавливает текущую дату и время в поле модели.
    """

    setattr(instance, field_name, timezone.now())


def clear_field(instance: models.Model, field_name: str) -> None:
    """
    Очищает поле модели, устанавливая None.
    """

    setattr(instance, field_name, None)


def clear_fields(instance: models.Model, field_names: list[str] | tuple[str, ...]) -> None:
    """
    Очищает несколько полей модели.
    """

    for field_name in field_names:
        clear_field(instance, field_name)


def has_model_field(instance: models.Model, field_name: str) -> bool:
    """
    Проверяет, есть ли поле у модели.
    """

    return any(
        field.name == field_name
        for field in instance._meta.fields
    )