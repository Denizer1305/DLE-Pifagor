from __future__ import annotations

from apps.testing.constants import AttemptCheckStatus, TestAttemptStatus
from apps.testing.models import TestAttempt
from django.db.models import Count, Q


def review_queue_queryset(
    *,
    teacher_id: int | None = None,
    test_id: int | None = None,
):
    """
    Возвращает очередь попыток, требующих проверки преподавателем.
    """

    queryset = (
        TestAttempt.objects.filter(
            Q(status=TestAttemptStatus.NEEDS_REVIEW)
            | Q(check_status=AttemptCheckStatus.NEEDS_REVIEW)
            | Q(requires_manual_review=True)
            | Q(answers__requires_manual_review=True)
        )
        .select_related(
            "test",
            "test__course",
            "learner",
            "reviewer_teacher",
        )
        .prefetch_related(
            "answers",
            "answers__question",
        )
        .annotate(
            manual_answers_count=Count(
                "answers",
                filter=Q(answers__requires_manual_review=True),
                distinct=True,
            )
        )
        .distinct()
    )

    if teacher_id is not None:
        queryset = queryset.filter(test__owner_teacher_id=teacher_id)

    if test_id is not None:
        queryset = queryset.filter(test_id=test_id)

    return queryset.order_by(
        "-submitted_at",
        "-created_at",
        "-id",
    )


def get_review_queue_count(
    *,
    teacher_id: int | None = None,
    test_id: int | None = None,
) -> int:
    """
    Возвращает количество попыток в очереди проверки.
    """

    return review_queue_queryset(
        teacher_id=teacher_id,
        test_id=test_id,
    ).count()
