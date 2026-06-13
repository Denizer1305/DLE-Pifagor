from __future__ import annotations

from decimal import Decimal

from apps.testing.constants import AttemptCheckStatus, TestAttemptStatus
from apps.testing.services.review import (
    build_teacher_testing_summary,
    build_test_review_summary,
    get_teacher_review_queue,
    get_teacher_review_queue_count,
    recalculate_attempt_score_from_answers,
)
from apps.testing.tests.factories import (
    create_answer,
    create_attempt,
    create_choice_question_with_options,
    create_result,
    create_teacher,
    create_test,
)
from django.test import TestCase


class ReviewQueueServicesTestCase(TestCase):
    """
    Тесты сервисов очереди проверки.
    """

    def test_get_teacher_review_queue_returns_attempts_for_teacher(self) -> None:
        """
        Очередь проверки возвращает попытки тестов преподавателя.
        """

        teacher = create_teacher()
        foreign_teacher = create_teacher()

        exam = create_test(owner_teacher=teacher)
        foreign_exam = create_test(owner_teacher=foreign_teacher)

        attempt = create_attempt(
            test=exam,
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
            requires_manual_review=True,
        )
        foreign_attempt = create_attempt(
            test=foreign_exam,
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
            requires_manual_review=True,
        )

        queryset = get_teacher_review_queue(teacher_id=teacher.id)

        self.assertIn(attempt, queryset)
        self.assertNotIn(foreign_attempt, queryset)

    def test_get_teacher_review_queue_count_returns_count(self) -> None:
        """
        Сервис возвращает количество попыток в очереди проверки.
        """

        teacher = create_teacher()
        exam = create_test(owner_teacher=teacher)

        create_attempt(
            test=exam,
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
            requires_manual_review=True,
        )

        queue_count = get_teacher_review_queue_count(teacher_id=teacher.id)

        self.assertEqual(queue_count, 1)


class ReviewSummaryServicesTestCase(TestCase):
    """
    Тесты сервисов summary по тестированию.
    """

    def test_build_test_review_summary_returns_expected_keys(self) -> None:
        """
        Сводка по тесту возвращает основные показатели.
        """

        exam = create_test()

        create_attempt(
            test=exam,
            status=TestAttemptStatus.CONFIRMED,
            is_confirmed_by_teacher=True,
            final_score=Decimal("80"),
            final_grade=4,
        )
        create_result(
            test=exam,
            learner=create_attempt(test=exam).learner,
            attempts_count=1,
            confirmed_attempts_count=1,
            average_score=Decimal("80"),
            average_grade=Decimal("4"),
            best_score=Decimal("80"),
            best_grade=4,
            is_passed=True,
            is_visible_to_learner=True,
        )

        summary = build_test_review_summary(test_id=exam.id)

        self.assertIn("attempts_count", summary)
        self.assertIn("learners_count", summary)
        self.assertIn("average_final_grade", summary)
        self.assertGreaterEqual(summary["attempts_count"], 1)

    def test_build_teacher_testing_summary_returns_expected_keys(self) -> None:
        """
        Сводка преподавателя возвращает основные показатели.
        """

        teacher = create_teacher()
        exam = create_test(owner_teacher=teacher)

        create_attempt(
            test=exam,
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
            requires_manual_review=True,
        )

        summary = build_teacher_testing_summary(teacher_id=teacher.id)

        self.assertIn("attempts_count", summary)
        self.assertIn("needs_review_count", summary)
        self.assertIn("learners_count", summary)
        self.assertEqual(summary["needs_review_count"], 1)


class ReviewRecalculationServicesTestCase(TestCase):
    """
    Тесты пересчёта попытки по ответам.
    """

    def test_recalculate_attempt_score_from_answers_sets_final_values(self) -> None:
        """
        Сервис пересчитывает итоговый балл и оценку попытки.
        """

        exam = create_test(max_score=100)
        attempt = create_attempt(
            test=exam,
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
        )

        first_question = create_choice_question_with_options(
            test=exam,
            score=50,
        )
        second_question = create_choice_question_with_options(
            test=exam,
            score=50,
        )

        create_answer(
            attempt=attempt,
            question=first_question,
            final_score=Decimal("40"),
            requires_manual_review=False,
        )
        create_answer(
            attempt=attempt,
            question=second_question,
            final_score=Decimal("45"),
            requires_manual_review=False,
        )

        updated_attempt = recalculate_attempt_score_from_answers(
            attempt=attempt,
        )

        self.assertEqual(updated_attempt.final_score, Decimal("85"))
        self.assertEqual(updated_attempt.teacher_score, Decimal("85"))
        self.assertEqual(updated_attempt.final_grade, 5)
        self.assertEqual(updated_attempt.teacher_grade, 5)
        self.assertFalse(updated_attempt.requires_manual_review)
        self.assertEqual(updated_attempt.status, TestAttemptStatus.AUTO_CHECKED)

    def test_recalculate_attempt_keeps_needs_review_if_answer_requires_review(
        self,
    ) -> None:
        """
        Если есть непроверенный ответ, попытка остаётся в проверке.
        """

        exam = create_test(max_score=100)
        attempt = create_attempt(
            test=exam,
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
        )
        question = create_choice_question_with_options(test=exam)

        create_answer(
            attempt=attempt,
            question=question,
            final_score=Decimal("20"),
            requires_manual_review=True,
        )

        updated_attempt = recalculate_attempt_score_from_answers(
            attempt=attempt,
        )

        self.assertTrue(updated_attempt.requires_manual_review)
        self.assertEqual(updated_attempt.status, TestAttemptStatus.NEEDS_REVIEW)
        self.assertEqual(
            updated_attempt.check_status,
            AttemptCheckStatus.NEEDS_REVIEW,
        )
