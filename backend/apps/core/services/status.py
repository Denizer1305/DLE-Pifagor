from __future__ import annotations

from collections.abc import Iterable
from typing import Any, TypeVar

from apps.core.services.models import clean_and_save_model
from apps.core.services.timestamps import clear_field, clear_fields, set_now
from django.db import models

ModelT = TypeVar("ModelT", bound=models.Model)


def set_status(
    instance: ModelT,
    *,
    status: str,
    status_field: str = "status",
    extra_fields: dict[str, Any] | None = None,
    update_fields: Iterable[str] | None = None,
    clean: bool = True,
) -> ModelT:
    """
    Технически меняет статус модели.

    Бизнес-проверки должны выполняться в доменном сервисе до вызова helper.
    """

    setattr(instance, status_field, status)

    changed_fields = [status_field]

    for field_name, value in (extra_fields or {}).items():
        setattr(instance, field_name, value)
        changed_fields.append(field_name)

    if update_fields is not None:
        changed_fields.extend(update_fields)

    if clean:
        return clean_and_save_model(
            instance,
            update_fields=changed_fields,
        )

    instance.save(update_fields=changed_fields)
    return instance


def set_status_with_timestamp(
    instance: ModelT,
    *,
    status: str,
    timestamp_field: str,
    status_field: str = "status",
    extra_fields: dict[str, Any] | None = None,
    clean: bool = True,
) -> ModelT:
    """
    Меняет статус и выставляет timestamp-поле текущим временем.
    """

    set_now(instance, timestamp_field)

    return set_status(
        instance,
        status=status,
        status_field=status_field,
        extra_fields=extra_fields,
        update_fields=[timestamp_field],
        clean=clean,
    )


def clear_status_timestamp(
    instance: ModelT,
    *,
    timestamp_field: str,
) -> None:
    """
    Очищает timestamp-поле статуса.
    """

    clear_field(instance, timestamp_field)


def clear_status_timestamps(
    instance: ModelT,
    *,
    timestamp_fields: list[str] | tuple[str, ...],
) -> None:
    """
    Очищает несколько timestamp-полей статуса.
    """

    clear_fields(instance, timestamp_fields)
