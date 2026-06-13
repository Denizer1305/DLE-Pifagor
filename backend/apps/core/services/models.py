from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any, TypeVar

from django.db import models

from apps.core.services.timestamps import has_model_field

ModelT = TypeVar("ModelT", bound=models.Model)

PROTECTED_MODEL_FIELD_NAMES = {
    "id",
    "pk",
}
"""Поля, которые нельзя менять через общий helper обновления."""


def normalize_update_fields(
    instance: models.Model,
    field_names: Iterable[str],
) -> list[str]:
    """
    Нормализует список полей для save(update_fields=...).

    Если у модели есть updated_at, поле добавляется автоматически,
    чтобы auto_now корректно фиксировал изменение.
    """

    normalized = list(dict.fromkeys(field_names))

    if normalized and has_model_field(instance, "updated_at"):
        if "updated_at" not in normalized:
            normalized.append("updated_at")

    return normalized


def apply_model_fields(
    instance: ModelT,
    data: Mapping[str, Any],
    *,
    allowed_fields: Iterable[str] | None = None,
    ignored_fields: Iterable[str] | None = None,
) -> list[str]:
    """
    Применяет данные к модели и возвращает список изменённых полей.

    Helper не вызывает full_clean и save. Он только выставляет значения.
    """

    allowed_field_set = set(allowed_fields) if allowed_fields is not None else None
    ignored_field_set = set(ignored_fields or ())
    changed_fields: list[str] = []

    for field_name, value in data.items():
        if field_name in PROTECTED_MODEL_FIELD_NAMES:
            continue

        if field_name in ignored_field_set:
            continue

        if allowed_field_set is not None and field_name not in allowed_field_set:
            continue

        current_value = getattr(instance, field_name, None)

        if current_value == value:
            continue

        setattr(instance, field_name, value)
        changed_fields.append(field_name)

    return changed_fields


def clean_model(
    instance: ModelT,
    *,
    exclude: Iterable[str] | None = None,
    validate_unique: bool = True,
) -> ModelT:
    """
    Вызывает full_clean у модели и возвращает модель.
    """

    instance.full_clean(
        exclude=list(exclude) if exclude is not None else None,
        validate_unique=validate_unique,
    )

    return instance


def save_model(
    instance: ModelT,
    *,
    update_fields: Iterable[str] | None = None,
) -> ModelT:
    """
    Сохраняет модель.

    Если update_fields передан пустым списком, сохранение не выполняется.
    """

    if update_fields is None:
        instance.save()
        return instance

    normalized_fields = normalize_update_fields(
        instance=instance,
        field_names=update_fields,
    )

    if not normalized_fields:
        return instance

    instance.save(update_fields=normalized_fields)

    return instance


def clean_and_save_model(
    instance: ModelT,
    *,
    update_fields: Iterable[str] | None = None,
    exclude: Iterable[str] | None = None,
    validate_unique: bool = True,
) -> ModelT:
    """
    Валидирует и сохраняет модель.
    """

    clean_model(
        instance,
        exclude=exclude,
        validate_unique=validate_unique,
    )

    return save_model(
        instance,
        update_fields=update_fields,
    )


def create_model_instance(
    model_class: type[ModelT],
    data: Mapping[str, Any],
    *,
    exclude: Iterable[str] | None = None,
    validate_unique: bool = True,
) -> ModelT:
    """
    Создаёт модель из payload, валидирует и сохраняет её.
    """

    instance = model_class(**dict(data))

    return clean_and_save_model(
        instance,
        exclude=exclude,
        validate_unique=validate_unique,
    )


def update_model_instance(
    instance: ModelT,
    data: Mapping[str, Any],
    *,
    allowed_fields: Iterable[str] | None = None,
    ignored_fields: Iterable[str] | None = None,
    exclude: Iterable[str] | None = None,
    validate_unique: bool = True,
) -> ModelT:
    """
    Обновляет модель из payload, валидирует и сохраняет её.
    """

    changed_fields = apply_model_fields(
        instance=instance,
        data=data,
        allowed_fields=allowed_fields,
        ignored_fields=ignored_fields,
    )

    return clean_and_save_model(
        instance,
        update_fields=changed_fields,
        exclude=exclude,
        validate_unique=validate_unique,
    )