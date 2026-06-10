from __future__ import annotations

from apps.testing.selectors.question.base import question_detail_queryset
from django.shortcuts import get_object_or_404


def get_question_by_id(question_id: int):
    """
    Возвращает вопрос по идентификатору.
    """

    return get_object_or_404(
        question_detail_queryset(),
        id=question_id,
    )


def get_question_for_update(question_id: int):
    """
    Возвращает вопрос для изменения.
    """

    return get_object_or_404(
        question_detail_queryset().select_for_update(),
        id=question_id,
    )
