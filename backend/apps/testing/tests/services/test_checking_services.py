from __future__ import annotations

from decimal import Decimal

from apps.testing.constants import AttemptCheckStatus, TestAttemptStatus
from apps.testing.services import (
    auto_check_attempt,
    calculate_grade_from_score,
    confirm_attempt_result,
    review_attempt_answer,
)
from apps.testing.tests.factories import (
    create_answer,
    create_attempt,
    create_choice_question_with_options,
    create_teacher,
)
from django.test import TestCase


class TestCheckingServicesTestCase(TestCase):
    """
    Тесты сервисов проверки теста.
    """

    def test_calculate_grade_from_score_returns_grade(self) -> None:
        """
        Сервис рассчитывает предварительную оценку по баллам.
        """

        self.assertEqual(
            calculate_grade_from_score(
                score=85,
                max_score=100,
            ),
            5,
        )
        self.assertEqual(
            calculate_grade_from_score(
                score=70,
                max_score=100,
            ),
            4,
        )
        self.assertEqual(
            calculate_grade_from_score(
                score=50,
                max_score=100,
            ),
            3,
        )
        self.assertEqual(
            calculate_grade_from_score(
                score=20,
                max_score=100,
            ),
            2,
        )

    def test_auto_check_attempt_sets_auto_checked_status(self) -> None:
        """
        Автопроверка выставляет балл и статус.
        """

        attempt = create_attempt(status=TestAttemptStatus.SUBMITTED)
        question = create_choice_question_with_options(
            test=attempt.test,
            score=10,
        )
        option = question.options.filter(is_correct=True).first()

        create_answer(
            attempt=attempt,
            question=question,
            selected_option=option,
        )

        checked_attempt = auto_check_attempt(attempt=attempt)

        self.assertEqual(
            checked_attempt.status,
            TestAttemptStatus.AUTO_CHECKED,
        )
        self.assertEqual(
            checked_attempt.check_status,
            AttemptCheckStatus.AUTO_CHECKED,
        )
        self.assertEqual(checked_attempt.auto_score, Decimal("10"))

    def test_review_attempt_answer_sets_teacher_score(self) -> None:
        """
        Ручная проверка ответа фиксирует балл преподавателя.
        """

        answer = create_answer(requires_manual_review=True)

        reviewed_answer = review_attempt_answer(
            answer=answer,
            teacher_score=1,
            teacher_comment="Верно.",
        )

        self.assertEqual(reviewed_answer.teacher_score, 1)
        self.assertEqual(reviewed_answer.final_score, 1)
        self.assertFalse(reviewed_answer.requires_manual_review)
        self.assertEqual(reviewed_answer.teacher_comment, "Верно.")

    def test_confirm_attempt_result_sets_final_grade(self) -> None:
        """
        Преподаватель подтверждает итоговую оценку попытки.
        """

        teacher = create_teacher()
        attempt = create_attempt(
            status=TestAttemptStatus.AUTO_CHECKED,
            auto_score=80,
            auto_grade=4,
        )

        confirmed_attempt = confirm_attempt_result(
            attempt=attempt,
            reviewer_teacher=teacher,
            final_score=80,
            final_grade=4,
            teacher_comment="Оценка подтверждена.",
        )

        self.assertEqual(
            confirmed_attempt.status,
            TestAttemptStatus.CONFIRMED,
        )
        self.assertTrue(confirmed_attempt.is_confirmed_by_teacher)
        self.assertEqual(confirmed_attempt.final_grade, 4)
        self.assertEqual(confirmed_attempt.reviewer_teacher, teacher)
