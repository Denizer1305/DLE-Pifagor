from __future__ import annotations

from apps.testing.models import TestQuestion, TestQuestionOption


def taking_question_list_queryset(
    *,
    test_id: int,
):
    """
    Возвращает активные вопросы теста для прохождения учеником.
    """

    return (
        TestQuestion.objects.filter(
            test_id=test_id,
            is_active=True,
        )
        .select_related(
            "test",
            "source_bank_item",
        )
        .prefetch_related(
            "options",
        )
        .order_by(
            "order",
            "id",
        )
    )


def taking_option_list_queryset(
    *,
    question_id: int,
):
    """
    Возвращает активные варианты ответа для прохождения учеником.
    """

    return (
        TestQuestionOption.objects.filter(
            question_id=question_id,
            is_active=True,
        )
        .select_related(
            "question",
        )
        .order_by(
            "order",
            "id",
        )
    )


def taking_options_for_test_queryset(
    *,
    test_id: int,
):
    """
    Возвращает активные варианты ответов всех вопросов теста.
    """

    return (
        TestQuestionOption.objects.filter(
            question__test_id=test_id,
            question__is_active=True,
            is_active=True,
        )
        .select_related(
            "question",
        )
        .order_by(
            "question_id",
            "order",
            "id",
        )
    )
