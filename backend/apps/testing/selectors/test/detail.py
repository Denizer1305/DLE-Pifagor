from __future__ import annotations

from apps.testing.selectors.test.base import test_detail_queryset
from django.shortcuts import get_object_or_404


def get_test_by_id(test_id: int):
    """
    Возвращает тест по идентификатору.
    """

    return get_object_or_404(
        test_detail_queryset(),
        id=test_id,
    )


def get_test_for_update(test_id: int):
    """
    Возвращает тест для изменения.
    """

    return get_object_or_404(
        test_detail_queryset().select_for_update(),
        id=test_id,
    )
