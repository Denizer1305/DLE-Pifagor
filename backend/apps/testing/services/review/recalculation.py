from __future__ import annotations

from decimal import Decimal

from apps.testing.constants import AttemptCheckStatus, TestAttemptStatus
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def recalculate_attempt_score_from_answers(*, attempt):
    """
    Пересчитывает итоговые баллы попытки по ответам.

    Используется после ручной проверки отдельных ответов.
    """

    answers = list(attempt.answers.all())

    final_score = _calculate_final_score(answers=answers)
    requires_manual_review = _has_answers_for_manual_review(answers=answers)

    attempt.final_score = final_score
    attempt.teacher_score = final_score
    attempt.final_grade = _calculate_grade_from_score(
        score=final_score,
        max_score=attempt.test.max_score,
    )
    attempt.teacher_grade = attempt.final_grade
    attempt.requires_manual_review = requires_manual_review

    if requires_manual_review:
        attempt.status = TestAttemptStatus.NEEDS_REVIEW
        attempt.check_status = AttemptCheckStatus.NEEDS_REVIEW
    else:
        attempt.status = TestAttemptStatus.AUTO_CHECKED
        attempt.check_status = AttemptCheckStatus.CHECKED
        attempt.reviewed_at = timezone.now()

    attempt.full_clean()
    attempt.save(
        update_fields=[
            "final_score",
            "teacher_score",
            "final_grade",
            "teacher_grade",
            "requires_manual_review",
            "status",
            "check_status",
            "reviewed_at",
            "updated_at",
        ]
    )

    return attempt


def _calculate_final_score(*, answers: list) -> Decimal:
    """
    Считает итоговый балл по ответам.
    """

    total = Decimal("0")

    for answer in answers:
        if answer.final_score is not None:
            total += answer.final_score
            continue

        if answer.teacher_score is not None:
            total += answer.teacher_score
            continue

        total += answer.auto_score or Decimal("0")

    return total


def _has_answers_for_manual_review(*, answers: list) -> bool:
    """
    Проверяет, остались ли ответы, требующие ручной проверки.
    """

    return any(answer.requires_manual_review for answer in answers)


def _calculate_grade_from_score(
    *,
    score: Decimal,
    max_score: int,
) -> int:
    """
    Рассчитывает оценку по проценту выполнения.
    """

    if max_score <= 0:
        return 2

    percent = Decimal(score) / Decimal(max_score) * Decimal("100")

    if percent >= 85:
        return 5

    if percent >= 70:
        return 4

    if percent >= 50:
        return 3

    return 2
