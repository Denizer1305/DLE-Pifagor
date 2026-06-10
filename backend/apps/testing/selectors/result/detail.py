from __future__ import annotations

from apps.testing.selectors.result.base import result_detail_queryset
from django.shortcuts import get_object_or_404


def get_result_by_id(result_id: int):
    """
    Возвращает итоговый результат по идентификатору.
    """

    return get_object_or_404(
        result_detail_queryset(),
        id=result_id,
    )


def get_result_for_update(result_id: int):
    """
    Возвращает итоговый результат для изменения.
    """

    return get_object_or_404(
        result_detail_queryset().select_for_update(),
        id=result_id,
    )


def get_result_by_test_and_learner(
    *,
    test_id: int,
    learner_id: int,
):
    """
    Возвращает итоговый результат по тесту и обучающемуся.
    """

    return get_object_or_404(
        result_detail_queryset(),
        test_id=test_id,
        learner_id=learner_id,
    )
