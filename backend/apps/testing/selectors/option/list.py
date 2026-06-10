from __future__ import annotations

from apps.testing.selectors.option.base import option_base_queryset


def option_list_queryset(
    *,
    question_id: int | None = None,
    is_correct: bool | None = None,
    is_active: bool | None = None,
):
    """
    Возвращает список вариантов ответа с базовыми фильтрами.
    """

    queryset = option_base_queryset()

    if question_id is not None:
        queryset = queryset.filter(question_id=question_id)

    if is_correct is not None:
        queryset = queryset.filter(is_correct=is_correct)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset.order_by(
        "question_id",
        "order",
        "id",
    )


def active_option_list_queryset(*, question_id: int | None = None):
    """
    Возвращает активные варианты ответа.
    """

    return option_list_queryset(
        question_id=question_id,
        is_active=True,
    )


def correct_option_list_queryset(*, question_id: int):
    """
    Возвращает правильные активные варианты ответа.
    """

    return option_list_queryset(
        question_id=question_id,
        is_correct=True,
        is_active=True,
    )
