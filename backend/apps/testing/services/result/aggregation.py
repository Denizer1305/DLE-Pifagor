from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal

from apps.testing.constants import GradeSource, LearnerResultStatus, TestAttemptStatus
from apps.testing.models import TestAttempt, TestLearnerResult
from django.db import transaction


@transaction.atomic
def recalculate_learner_result(
    *,
    test,
    learner,
) -> TestLearnerResult:
    """
    Пересчитывает итоговый результат обучающегося по тесту.

    В расчёт средней оценки идут только подтверждённые преподавателем попытки.
    """

    result, _ = TestLearnerResult.objects.get_or_create(
        test=test,
        learner=learner,
    )

    attempts_queryset = TestAttempt.objects.filter(
        test=test,
        learner=learner,
    ).exclude(
        status=TestAttemptStatus.CANCELLED,
    )

    confirmed_attempts = attempts_queryset.filter(
        is_confirmed_by_teacher=True,
        final_grade__isnull=False,
    )

    result.attempts_count = attempts_queryset.count()
    result.confirmed_attempts_count = confirmed_attempts.count()
    result.last_attempt = attempts_queryset.order_by(
        "-attempt_number",
        "-id",
    ).first()

    _apply_average_values(
        result=result,
        confirmed_attempts=confirmed_attempts,
    )
    _apply_best_values(
        result=result,
        confirmed_attempts=confirmed_attempts,
    )
    _apply_blocking_state(
        result=result,
        test=test,
    )

    result.grade_source = GradeSource.AVERAGE
    result.full_clean()
    result.save()

    return result


def _apply_average_values(
    *,
    result: TestLearnerResult,
    confirmed_attempts,
) -> None:
    """
    Заполняет средний балл и среднюю оценку.
    """

    if not confirmed_attempts.exists():
        result.average_score = None
        result.average_grade = None
        result.is_passed = False
        return

    score_sum = sum(
        attempt.final_score or Decimal("0") for attempt in confirmed_attempts
    )
    grade_sum = sum(Decimal(str(attempt.final_grade)) for attempt in confirmed_attempts)

    attempts_count = Decimal(str(confirmed_attempts.count()))

    result.average_score = _round_decimal(score_sum / attempts_count)
    result.average_grade = _round_decimal(grade_sum / attempts_count)
    result.is_passed = result.average_score >= result.test.passing_score


def _apply_best_values(
    *,
    result: TestLearnerResult,
    confirmed_attempts,
) -> None:
    """
    Заполняет лучший балл и лучшую оценку.
    """

    best_attempt = confirmed_attempts.order_by(
        "-final_score",
        "-final_grade",
        "-attempt_number",
    ).first()

    if best_attempt is None:
        result.best_score = None
        result.best_grade = None
        return

    result.best_score = best_attempt.final_score
    result.best_grade = best_attempt.final_grade


def _apply_blocking_state(
    *,
    result: TestLearnerResult,
    test,
) -> None:
    """
    Блокирует повторное прохождение после исчерпания попыток.
    """

    if result.attempts_count >= test.max_attempts:
        result.status = LearnerResultStatus.BLOCKED
        result.is_blocked = True
        return

    result.status = LearnerResultStatus.ACTIVE
    result.is_blocked = False


def _round_decimal(value) -> Decimal:
    """
    Округляет Decimal до двух знаков.
    """

    return Decimal(value).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )
