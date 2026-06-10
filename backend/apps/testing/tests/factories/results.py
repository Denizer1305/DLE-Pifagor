from __future__ import annotations

from decimal import Decimal

from apps.course.tests.factories import create_learner
from apps.testing.constants import GradeSource, LearnerResultStatus
from apps.testing.models import TestLearnerResult
from apps.testing.tests.factories.attempts import create_attempt
from apps.testing.tests.factories.structure import create_test


def create_result(
    *,
    test=None,
    learner=None,
    last_attempt=None,
    **overrides,
) -> TestLearnerResult:
    """
    Создаёт итоговый результат обучающегося по тесту.
    """

    test = test or create_test()
    learner = learner or create_learner()
    last_attempt = last_attempt or create_attempt(
        test=test,
        learner=learner,
    )

    data = {
        "test": test,
        "learner": learner,
        "status": overrides.pop("status", LearnerResultStatus.ACTIVE),
        "grade_source": overrides.pop("grade_source", GradeSource.AVERAGE),
        "confirmed_attempts_count": overrides.pop(
            "confirmed_attempts_count",
            0,
        ),
        "attempts_count": overrides.pop("attempts_count", 1),
        "average_score": overrides.pop("average_score", None),
        "average_grade": overrides.pop("average_grade", None),
        "best_score": overrides.pop("best_score", None),
        "best_grade": overrides.pop("best_grade", None),
        "last_attempt": last_attempt,
        "is_passed": overrides.pop("is_passed", False),
        "is_blocked": overrides.pop("is_blocked", False),
        "is_visible_to_learner": overrides.pop(
            "is_visible_to_learner",
            False,
        ),
        "is_visible_to_guardian": overrides.pop(
            "is_visible_to_guardian",
            False,
        ),
    }
    data.update(overrides)

    return TestLearnerResult.objects.create(**data)


def create_visible_result(
    *,
    test=None,
    learner=None,
    **overrides,
) -> TestLearnerResult:
    """
    Создаёт опубликованный итоговый результат.
    """

    return create_result(
        test=test,
        learner=learner,
        confirmed_attempts_count=overrides.pop(
            "confirmed_attempts_count",
            1,
        ),
        attempts_count=overrides.pop("attempts_count", 1),
        average_score=overrides.pop("average_score", Decimal("80")),
        average_grade=overrides.pop("average_grade", Decimal("4")),
        best_score=overrides.pop("best_score", Decimal("80")),
        best_grade=overrides.pop("best_grade", 4),
        is_passed=overrides.pop("is_passed", True),
        is_visible_to_learner=overrides.pop(
            "is_visible_to_learner",
            True,
        ),
        is_visible_to_guardian=overrides.pop(
            "is_visible_to_guardian",
            True,
        ),
        **overrides,
    )
