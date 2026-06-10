from __future__ import annotations

from decimal import Decimal

from apps.testing.constants import (
    AttemptCheckStatus,
    QuestionCheckMode,
    QuestionType,
    TestAttemptStatus,
)
from apps.testing.models import TestAttempt, TestAttemptAnswer
from apps.testing.services.checking.grading import calculate_grade_from_score
from apps.testing.validators import validate_attempt_can_be_checked
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def auto_check_attempt(*, attempt: TestAttempt) -> TestAttempt:
    """
    Выполняет автоматическую проверку попытки.
    """

    validate_attempt_can_be_checked(attempt=attempt)

    total_score = Decimal("0")
    requires_manual_review = False

    for answer in attempt.answers.select_related("question", "selected_option"):
        checked_answer = auto_check_answer(answer=answer)
        total_score += checked_answer.auto_score

        if checked_answer.requires_manual_review:
            requires_manual_review = True

    attempt.auto_score = total_score
    attempt.auto_grade = calculate_grade_from_score(
        score=total_score,
        max_score=attempt.test.max_score,
    )
    attempt.requires_manual_review = requires_manual_review
    attempt.auto_checked_at = timezone.now()

    if requires_manual_review:
        attempt.status = TestAttemptStatus.NEEDS_REVIEW
        attempt.check_status = AttemptCheckStatus.NEEDS_REVIEW
    else:
        attempt.status = TestAttemptStatus.AUTO_CHECKED
        attempt.check_status = AttemptCheckStatus.AUTO_CHECKED

    attempt.full_clean()
    attempt.save(
        update_fields=[
            "auto_score",
            "auto_grade",
            "requires_manual_review",
            "auto_checked_at",
            "status",
            "check_status",
            "updated_at",
        ]
    )

    return attempt


def auto_check_answer(*, answer: TestAttemptAnswer) -> TestAttemptAnswer:
    """
    Выполняет автоматическую проверку одного ответа.
    """

    question_type = answer.question.question_type

    if answer.question.check_mode == QuestionCheckMode.MANUAL:
        return _mark_answer_for_manual_review(answer=answer)

    if question_type == QuestionType.SINGLE_CHOICE:
        return _check_single_choice_answer(answer=answer)

    if question_type == QuestionType.TRUE_FALSE:
        return _check_single_choice_answer(answer=answer)

    if question_type == QuestionType.MULTIPLE_CHOICE:
        return _check_multiple_choice_answer(answer=answer)

    if question_type == QuestionType.NUMBER:
        return _check_number_answer(answer=answer)

    if question_type == QuestionType.SHORT_TEXT:
        return _check_short_text_answer(answer=answer)

    return _mark_answer_for_manual_review(answer=answer)


def _check_single_choice_answer(*, answer: TestAttemptAnswer) -> TestAttemptAnswer:
    """
    Проверяет вопрос с одним выбранным вариантом.
    """

    is_correct = bool(answer.selected_option and answer.selected_option.is_correct)

    return _apply_auto_answer_result(
        answer=answer,
        is_correct=is_correct,
    )


def _check_multiple_choice_answer(*, answer: TestAttemptAnswer) -> TestAttemptAnswer:
    """
    Проверяет вопрос с несколькими вариантами.
    """

    selected_ids = {int(option_id) for option_id in answer.selected_options_data or []}
    correct_ids = set(
        answer.question.options.filter(
            is_active=True,
            is_correct=True,
        ).values_list(
            "id",
            flat=True,
        )
    )

    return _apply_auto_answer_result(
        answer=answer,
        is_correct=selected_ids == correct_ids,
    )


def _check_number_answer(*, answer: TestAttemptAnswer) -> TestAttemptAnswer:
    """
    Проверяет числовой ответ.
    """

    is_correct = (
        answer.number_answer is not None
        and answer.question.expected_number_answer is not None
        and answer.number_answer == answer.question.expected_number_answer
    )

    return _apply_auto_answer_result(
        answer=answer,
        is_correct=is_correct,
    )


def _check_short_text_answer(*, answer: TestAttemptAnswer) -> TestAttemptAnswer:
    """
    Полуавтоматически проверяет короткий текстовый ответ.
    """

    expected_answer = answer.question.expected_text_answer.strip()

    if not expected_answer:
        return _mark_answer_for_manual_review(answer=answer)

    user_answer = answer.text_answer.strip()

    if not answer.question.case_sensitive:
        expected_answer = expected_answer.lower()
        user_answer = user_answer.lower()

    return _apply_auto_answer_result(
        answer=answer,
        is_correct=user_answer == expected_answer,
    )


def _apply_auto_answer_result(
    *,
    answer: TestAttemptAnswer,
    is_correct: bool,
) -> TestAttemptAnswer:
    """
    Применяет результат автоматической проверки ответа.
    """

    answer.is_correct = is_correct
    answer.auto_score = Decimal(answer.question.score) if is_correct else Decimal("0")
    answer.final_score = answer.auto_score
    answer.requires_manual_review = False

    answer.full_clean()
    answer.save(
        update_fields=[
            "is_correct",
            "auto_score",
            "final_score",
            "requires_manual_review",
            "updated_at",
        ]
    )

    return answer


def _mark_answer_for_manual_review(
    *,
    answer: TestAttemptAnswer,
) -> TestAttemptAnswer:
    """
    Помечает ответ как требующий ручной проверки.
    """

    answer.is_correct = None
    answer.auto_score = Decimal("0")
    answer.final_score = None
    answer.requires_manual_review = True

    answer.full_clean()
    answer.save(
        update_fields=[
            "is_correct",
            "auto_score",
            "final_score",
            "requires_manual_review",
            "updated_at",
        ]
    )

    return answer
