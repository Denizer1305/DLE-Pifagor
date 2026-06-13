from __future__ import annotations

from decimal import Decimal

from apps.testing.constants import (
    AttemptCheckStatus,
    LearnerResultStatus,
    TestAttemptStatus,
)
from apps.testing.selectors import (
    get_review_queue_count,
    review_queue_queryset,
    teacher_testing_summary,
)
from apps.testing.selectors import (
    test_review_summary as build_test_review_summary_selector,
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


class ReviewQueueSelectorsTestCase(TestCase):
    """
    Тесты селекторов очереди проверки.
    """

    def test_review_queue_queryset_returns_attempts_that_need_review(self) -> None:
        """
        Селектор возвращает попытки, требующие проверки.
        """

        review_attempt = create_attempt(
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
            requires_manual_review=True,
        )
        started_attempt = create_attempt(
            status=TestAttemptStatus.STARTED,
            check_status=AttemptCheckStatus.NOT_CHECKED,
            requires_manual_review=False,
        )

        queryset = review_queue_queryset()

        self.assertIn(review_attempt, queryset)
        self.assertNotIn(started_attempt, queryset)

    def test_review_queue_queryset_filters_by_teacher(self) -> None:
        """
        Селектор фильтрует очередь проверки по преподавателю.
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

        queryset = review_queue_queryset(teacher_id=teacher.id)

        self.assertIn(attempt, queryset)
        self.assertNotIn(foreign_attempt, queryset)

    def test_review_queue_queryset_filters_by_test(self) -> None:
        """
        Селектор фильтрует очередь проверки по тесту.
        """

        exam = create_test()
        foreign_exam = create_test()

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

        queryset = review_queue_queryset(test_id=exam.id)

        self.assertIn(attempt, queryset)
        self.assertNotIn(foreign_attempt, queryset)

    def test_review_queue_queryset_counts_manual_answers(self) -> None:
        """
        Селектор добавляет количество ответов, требующих ручной проверки.
        """

        attempt = create_attempt(
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
            requires_manual_review=True,
        )
        question = create_choice_question_with_options(test=attempt.test)

        create_answer(
            attempt=attempt,
            question=question,
            requires_manual_review=True,
        )

        found_attempt = review_queue_queryset().get(id=attempt.id)

        self.assertEqual(found_attempt.manual_answers_count, 1)

    def test_get_review_queue_count_returns_count(self) -> None:
        """
        Селектор возвращает количество попыток в очереди.
        """

        create_attempt(
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
            requires_manual_review=True,
        )
        create_attempt(
            status=TestAttemptStatus.STARTED,
            check_status=AttemptCheckStatus.NOT_CHECKED,
        )

        count = get_review_queue_count()

        self.assertEqual(count, 1)


class ReviewSummarySelectorsTestCase(TestCase):
    """
    Тесты селекторов summary по тестированию.
    """

    def test_test_review_summary_returns_attempt_counters(self) -> None:
        """
        Сводка по тесту возвращает счётчики попыток.
        """

        exam = create_test()

        create_attempt(
            test=exam,
            status=TestAttemptStatus.STARTED,
        )
        create_attempt(
            test=exam,
            status=TestAttemptStatus.CONFIRMED,
            final_score=Decimal("80"),
            final_grade=4,
        )
        create_attempt(
            status=TestAttemptStatus.CONFIRMED,
            final_score=Decimal("90"),
            final_grade=5,
        )

        summary = build_test_review_summary_selector(test_id=exam.id)

        self.assertEqual(summary["attempts_count"], 2)
        self.assertEqual(summary["started_count"], 1)
        self.assertEqual(summary["confirmed_count"], 1)

    def test_test_review_summary_returns_result_counters(self) -> None:
        """
        Сводка по тесту возвращает счётчики результатов.
        """

        exam = create_test()
        attempt = create_attempt(
            test=exam,
            status=TestAttemptStatus.CONFIRMED,
            final_score=Decimal("80"),
            final_grade=4,
        )

        create_result(
            test=exam,
            learner=attempt.learner,
            last_attempt=attempt,
            attempts_count=1,
            confirmed_attempts_count=1,
            average_score=Decimal("80"),
            average_grade=Decimal("4"),
            best_score=Decimal("80"),
            best_grade=4,
            is_passed=True,
            is_visible_to_learner=True,
        )

        summary = build_test_review_summary_selector(test_id=exam.id)

        self.assertEqual(summary["learners_count"], 1)
        self.assertEqual(summary["passed_count"], 1)
        self.assertEqual(summary["visible_results_count"], 1)

    def test_teacher_testing_summary_filters_by_teacher(self) -> None:
        """
        Сводка преподавателя учитывает только его тесты.
        """

        teacher = create_teacher()
        foreign_teacher = create_teacher()

        exam = create_test(owner_teacher=teacher)
        foreign_exam = create_test(owner_teacher=foreign_teacher)

        create_attempt(
            test=exam,
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
            requires_manual_review=True,
        )
        create_attempt(
            test=foreign_exam,
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
            requires_manual_review=True,
        )

        summary = teacher_testing_summary(teacher_id=teacher.id)

        self.assertEqual(summary["attempts_count"], 1)
        self.assertEqual(summary["needs_review_count"], 1)

    def test_teacher_testing_summary_counts_blocked_results(self) -> None:
        """
        Сводка преподавателя считает заблокированные результаты.
        """

        teacher = create_teacher()
        exam = create_test(owner_teacher=teacher)
        attempt = create_attempt(test=exam)

        create_result(
            test=exam,
            learner=attempt.learner,
            last_attempt=attempt,
            status=LearnerResultStatus.BLOCKED,
            is_blocked=True,
        )

        summary = teacher_testing_summary(teacher_id=teacher.id)

        self.assertEqual(summary["blocked_count"], 1)
