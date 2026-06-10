from __future__ import annotations

from apps.testing.selectors.option.base import option_detail_queryset
from django.shortcuts import get_object_or_404


def get_option_by_id(option_id: int):
    """
    Возвращает вариант ответа по идентификатору.
    """

    return get_object_or_404(
        option_detail_queryset(),
        id=option_id,
    )


def get_option_for_update(option_id: int):
    """
    Возвращает вариант ответа для изменения.
    """

    return get_object_or_404(
        option_detail_queryset().select_for_update(),
        id=option_id,
    )
