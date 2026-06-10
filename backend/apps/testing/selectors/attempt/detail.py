from __future__ import annotations

from apps.testing.selectors.attempt.base import attempt_detail_queryset
from django.shortcuts import get_object_or_404


def get_attempt_by_id(attempt_id: int):
    """
    Возвращает попытку по идентификатору.
    """

    return get_object_or_404(
        attempt_detail_queryset(),
        id=attempt_id,
    )


def get_attempt_for_update(attempt_id: int):
    """
    Возвращает попытку для изменения.
    """

    return get_object_or_404(
        attempt_detail_queryset().select_for_update(),
        id=attempt_id,
    )


def get_attempt_by_test_learner_and_number(
    *,
    test_id: int,
    learner_id: int,
    attempt_number: int,
):
    """
    Возвращает попытку по тесту, обучающемуся и номеру.
    """

    return get_object_or_404(
        attempt_detail_queryset(),
        test_id=test_id,
        learner_id=learner_id,
        attempt_number=attempt_number,
    )
