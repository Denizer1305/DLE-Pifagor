from __future__ import annotations

from apps.testing.constants import LearnerResultStatus, TestAttemptStatus
from apps.testing.models import TestAttempt, TestLearnerResult
from django.db.models import Avg, Count, Q


def test_review_summary(
    *,
    test_id: int,
) -> dict:
    """
    Возвращает сводку по тесту для преподавателя.
    """

    attempts_queryset = TestAttempt.objects.filter(test_id=test_id)
    results_queryset = TestLearnerResult.objects.filter(test_id=test_id)

    attempts_summary = attempts_queryset.aggregate(
        attempts_count=Count("id"),
        started_count=Count(
            "id",
            filter=Q(status=TestAttemptStatus.STARTED),
        ),
        submitted_count=Count(
            "id",
            filter=Q(status=TestAttemptStatus.SUBMITTED),
        ),
        needs_review_count=Count(
            "id",
            filter=Q(status=TestAttemptStatus.NEEDS_REVIEW),
        ),
        confirmed_count=Count(
            "id",
            filter=Q(status=TestAttemptStatus.CONFIRMED),
        ),
        published_count=Count(
            "id",
            filter=Q(status=TestAttemptStatus.PUBLISHED),
        ),
        expired_count=Count(
            "id",
            filter=Q(status=TestAttemptStatus.EXPIRED),
        ),
        cancelled_count=Count(
            "id",
            filter=Q(status=TestAttemptStatus.CANCELLED),
        ),
        average_final_score=Avg("final_score"),
        average_final_grade=Avg("final_grade"),
    )

    results_summary = results_queryset.aggregate(
        learners_count=Count("learner", distinct=True),
        passed_count=Count(
            "id",
            filter=Q(is_passed=True),
        ),
        failed_count=Count(
            "id",
            filter=Q(is_passed=False),
        ),
        blocked_count=Count(
            "id",
            filter=Q(status=LearnerResultStatus.BLOCKED),
        ),
        visible_results_count=Count(
            "id",
            filter=Q(is_visible_to_learner=True),
        ),
        average_score=Avg("average_score"),
        average_grade=Avg("average_grade"),
    )

    return {
        **attempts_summary,
        **results_summary,
    }


def teacher_testing_summary(
    *,
    teacher_id: int,
) -> dict:
    """
    Возвращает общую сводку по тестированию преподавателя.
    """

    attempts_queryset = TestAttempt.objects.filter(
        test__owner_teacher_id=teacher_id,
    )
    results_queryset = TestLearnerResult.objects.filter(
        test__owner_teacher_id=teacher_id,
    )

    attempts_summary = attempts_queryset.aggregate(
        attempts_count=Count("id"),
        needs_review_count=Count(
            "id",
            filter=Q(
                Q(status=TestAttemptStatus.NEEDS_REVIEW)
                | Q(requires_manual_review=True)
                | Q(answers__requires_manual_review=True)
            ),
            distinct=True,
        ),
        confirmed_count=Count(
            "id",
            filter=Q(status=TestAttemptStatus.CONFIRMED),
        ),
        published_count=Count(
            "id",
            filter=Q(status=TestAttemptStatus.PUBLISHED),
        ),
        average_final_grade=Avg("final_grade"),
    )

    results_summary = results_queryset.aggregate(
        learners_count=Count("learner", distinct=True),
        blocked_count=Count(
            "id",
            filter=Q(status=LearnerResultStatus.BLOCKED),
        ),
        average_grade=Avg("average_grade"),
    )

    return {
        **attempts_summary,
        **results_summary,
    }
