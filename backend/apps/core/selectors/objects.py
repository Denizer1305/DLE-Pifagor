from __future__ import annotations

from typing import Any, TypeVar

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404

ModelT = TypeVar("ModelT", bound=models.Model)


def get_object_or_none(
    queryset: models.QuerySet[ModelT] | models.Manager[ModelT],
    **filters: Any,
) -> ModelT | None:
    """
    Возвращает объект по фильтрам или None.

    Используется в selectors и services, где отсутствие объекта
    не всегда является ошибкой.
    """

    try:
        return queryset.get(**filters)
    except ObjectDoesNotExist:
        return None


def get_required_object(
    queryset: models.QuerySet[ModelT] | models.Manager[ModelT],
    *,
    message: str | None = None,
    **filters: Any,
) -> ModelT:
    """
    Возвращает объект по фильтрам или выбрасывает Http404.

    Используется в detail selectors, где отсутствие объекта должно
    корректно превращаться в 404 на уровне API.
    """

    obj = get_object_or_none(queryset, **filters)

    if obj is None:
        raise Http404(message or "Объект не найден.")

    return obj


def object_exists(
    queryset: models.QuerySet[ModelT] | models.Manager[ModelT],
    **filters: Any,
) -> bool:
    """
    Проверяет существование объекта по фильтрам.
    """

    return queryset.filter(**filters).exists()