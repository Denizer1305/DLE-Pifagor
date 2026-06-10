from __future__ import annotations

from apps.testing.selectors.answer.base import answer_detail_queryset
from django.shortcuts import get_object_or_404


def get_answer_by_id(answer_id: int):
    """
    Возвращает ответ по идентификатору.
    """

    return get_object_or_404(
        answer_detail_queryset(),
        id=answer_id,
    )


def get_answer_for_update(answer_id: int):
    """
    Возвращает ответ для изменения.
    """

    return get_object_or_404(
        answer_detail_queryset().select_for_update(),
        id=answer_id,
    )


def get_answer_by_attempt_and_question(
    *,
    attempt_id: int,
    question_id: int,
):
    """
    Возвращает ответ по попытке и вопросу.
    """

    return get_object_or_404(
        answer_detail_queryset(),
        attempt_id=attempt_id,
        question_id=question_id,
    )
