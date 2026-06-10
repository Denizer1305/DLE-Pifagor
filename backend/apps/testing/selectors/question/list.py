from __future__ import annotations

from apps.testing.selectors.question.base import question_base_queryset
from django.db.models import Q


def question_list_queryset(
    *,
    test_id: int | None = None,
    question_type: str | None = None,
    check_mode: str | None = None,
    search: str | None = None,
    is_active: bool | None = None,
):
    """
    Возвращает список вопросов с базовыми фильтрами.
    """

    queryset = question_base_queryset()

    if test_id is not None:
        queryset = queryset.filter(test_id=test_id)

    if question_type:
        queryset = queryset.filter(question_type=question_type)

    if check_mode:
        queryset = queryset.filter(check_mode=check_mode)

    if search:
        queryset = queryset.filter(
            Q(title__icontains=search)
            | Q(text__icontains=search)
            | Q(explanation__icontains=search)
        )

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset.order_by(
        "test_id",
        "order",
        "id",
    )


def active_question_list_queryset(*, test_id: int | None = None):
    """
    Возвращает активные вопросы.
    """

    return question_list_queryset(
        test_id=test_id,
        is_active=True,
    )
