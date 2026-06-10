from __future__ import annotations

from apps.testing.constants import AttemptCheckStatus, TestAttemptStatus
from apps.testing.models import TestAttempt, TestAttemptAnswer
from apps.testing.validators import (
    validate_attempt_can_be_confirmed,
    validate_confirmation_values,
)
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def review_attempt_answer(
    *,
    answer: TestAttemptAnswer,
    teacher_score,
    teacher_comment: str = "",
) -> TestAttemptAnswer:
    """
    Фиксирует ручную проверку одного ответа.
    """

    answer.teacher_score = teacher_score
    answer.final_score = teacher_score
    answer.teacher_comment = teacher_comment
    answer.requires_manual_review = False
    answer.is_correct = teacher_score > 0

    answer.full_clean()
    answer.save(
        update_fields=[
            "teacher_score",
            "final_score",
            "teacher_comment",
            "requires_manual_review",
            "is_correct",
            "updated_at",
        ]
    )

    return answer


@transaction.atomic
def confirm_attempt_result(
    *,
    attempt: TestAttempt,
    reviewer_teacher,
    final_score,
    final_grade,
    teacher_comment: str = "",
) -> TestAttempt:
    """
    Подтверждает итоговую оценку попытки преподавателем.
    """

    validate_attempt_can_be_confirmed(attempt=attempt)
    validate_confirmation_values(
        final_score=final_score,
        final_grade=final_grade,
        max_score=attempt.test.max_score,
    )

    attempt.teacher_score = final_score
    attempt.teacher_grade = final_grade
    attempt.final_score = final_score
    attempt.final_grade = final_grade
    attempt.reviewer_teacher = reviewer_teacher
    attempt.teacher_comment = teacher_comment
    attempt.reviewed_at = timezone.now()
    attempt.confirmed_at = timezone.now()
    attempt.is_confirmed_by_teacher = True
    attempt.status = TestAttemptStatus.CONFIRMED
    attempt.check_status = AttemptCheckStatus.CHECKED

    attempt.full_clean()
    attempt.save(
        update_fields=[
            "teacher_score",
            "teacher_grade",
            "final_score",
            "final_grade",
            "reviewer_teacher",
            "teacher_comment",
            "reviewed_at",
            "confirmed_at",
            "is_confirmed_by_teacher",
            "status",
            "check_status",
            "updated_at",
        ]
    )

    return attempt
