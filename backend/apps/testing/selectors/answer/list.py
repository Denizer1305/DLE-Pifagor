from __future__ import annotations

from apps.testing.selectors.answer.base import answer_base_queryset


def answer_list_queryset(
    *,
    attempt_id: int | None = None,
    question_id: int | None = None,
    requires_manual_review: bool | None = None,
    is_correct: bool | None = None,
):
    """
    Возвращает список ответов с базовыми фильтрами.
    """

    queryset = answer_base_queryset()

    if attempt_id is not None:
        queryset = queryset.filter(attempt_id=attempt_id)

    if question_id is not None:
        queryset = queryset.filter(question_id=question_id)

    if requires_manual_review is not None:
        queryset = queryset.filter(
            requires_manual_review=requires_manual_review,
        )

    if is_correct is not None:
        queryset = queryset.filter(is_correct=is_correct)

    return queryset.order_by(
        "attempt_id",
        "question_id",
        "id",
    )


def attempt_answer_list_queryset(*, attempt_id: int):
    """
    Возвращает ответы конкретной попытки.
    """

    return answer_list_queryset(attempt_id=attempt_id)


def manual_review_answer_list_queryset(*, attempt_id: int | None = None):
    """
    Возвращает ответы, требующие ручной проверки.
    """

    return answer_list_queryset(
        attempt_id=attempt_id,
        requires_manual_review=True,
    )
