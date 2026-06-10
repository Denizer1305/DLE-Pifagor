from __future__ import annotations

from apps.testing.models import TestQuestion, TestQuestionOption
from django.db import transaction
from django.db.models import Max, QuerySet


@transaction.atomic
def reorder_questions(
    *,
    test_id: int,
    ordered_question_ids: list[int],
) -> None:
    """
    Переупорядочивает вопросы теста.
    """

    queryset = TestQuestion.objects.filter(test_id=test_id)

    _reorder_queryset_by_ids(
        queryset=queryset,
        ordered_ids=ordered_question_ids,
    )


@transaction.atomic
def reorder_question_options(
    *,
    question_id: int,
    ordered_option_ids: list[int],
) -> None:
    """
    Переупорядочивает варианты ответа.
    """

    queryset = TestQuestionOption.objects.filter(question_id=question_id)

    _reorder_queryset_by_ids(
        queryset=queryset,
        ordered_ids=ordered_option_ids,
    )


def _reorder_queryset_by_ids(
    *,
    queryset: QuerySet,
    ordered_ids: list[int],
) -> None:
    """
    Безопасно переставляет order без нарушения UNIQUE constraints.
    """

    if not ordered_ids:
        return

    existing_ids = set(
        queryset.filter(id__in=ordered_ids).values_list(
            "id",
            flat=True,
        )
    )

    ordered_existing_ids = [
        object_id for object_id in ordered_ids if object_id in existing_ids
    ]

    if not ordered_existing_ids:
        return

    max_order = queryset.aggregate(value=Max("order"))["value"] or 0
    temp_offset = max_order + len(ordered_existing_ids) + 1000

    for index, object_id in enumerate(ordered_existing_ids, start=1):
        queryset.filter(id=object_id).update(order=temp_offset + index)

    for index, object_id in enumerate(ordered_existing_ids, start=1):
        queryset.filter(id=object_id).update(order=index)
