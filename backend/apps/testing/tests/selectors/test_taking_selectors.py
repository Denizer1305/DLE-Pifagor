from __future__ import annotations

from django.test import TestCase

from apps.testing.constants import (
    TestAttemptStatus,
    TestStatus,
)
from apps.testing.selectors import (
    get_active_attempt_for_taking,
    get_taking_attempt_by_id,
    get_taking_test_by_id,
    taking_option_list_queryset,
    taking_options_for_test_queryset,
    taking_question_list_queryset,
    taking_test_queryset,
)
from apps.testing.tests.factories import (
    create_attempt,
    create_choice_question_with_options,
    create_learner,
    create_option,
    create_question,
    create_test,
)


class TakingTestSelectorsTestCase(TestCase):
    """
    Тесты селекторов тестов для прохождения.
    """

    def test_taking_test_queryset_returns_only_published_active_tests(self) -> None:
        """
        Селектор возвращает только опубликованные активные тесты.
        """

        published_exam = create_test(
            status=TestStatus.PUBLISHED,
            is_active=True,
        )
        draft_exam = create_test(
            status=TestStatus.DRAFT,
            is_active=True,
        )
        inactive_exam = create_test(
            status=TestStatus.PUBLISHED,
            is_active=False,
        )

        queryset = taking_test_queryset()

        self.assertIn(published_exam, queryset)
        self.assertNotIn(draft_exam, queryset)
        self.assertNotIn(inactive_exam, queryset)

    def test_get_taking_test_by_id_returns_published_active_test(self) -> None:
        """
        Селектор возвращает опубликованный активный тест по id.
        """

        exam = create_test(
            status=TestStatus.PUBLISHED,
            is_active=True,
        )

        found_exam = get_taking_test_by_id(exam.id)

        self.assertEqual(found_exam, exam)

    def test_get_active_attempt_for_taking_returns_started_attempt(self) -> None:
        """
        Селектор возвращает активную начатую попытку ученика.
        """

        exam = create_test()
        learner = create_learner()

        started_attempt = create_attempt(
            test=exam,
            learner=learner,
            status=TestAttemptStatus.STARTED,
        )
        submitted_attempt = create_attempt(
            test=exam,
            learner=learner,
            status=TestAttemptStatus.SUBMITTED,
        )

        found_attempt = get_active_attempt_for_taking(
            test_id=exam.id,
            learner_id=learner.id,
        )

        self.assertEqual(found_attempt, started_attempt)
        self.assertNotEqual(found_attempt, submitted_attempt)

    def test_get_active_attempt_for_taking_returns_none_without_started_attempt(
        self,
    ) -> None:
        """
        Селектор возвращает None, если активной попытки нет.
        """

        exam = create_test()
        learner = create_learner()

        create_attempt(
            test=exam,
            learner=learner,
            status=TestAttemptStatus.SUBMITTED,
        )

        found_attempt = get_active_attempt_for_taking(
            test_id=exam.id,
            learner_id=learner.id,
        )

        self.assertIsNone(found_attempt)

    def test_get_taking_attempt_by_id_returns_attempt_for_learner(self) -> None:
        """
        Селектор возвращает попытку конкретного ученика.
        """

        attempt = create_attempt()

        found_attempt = get_taking_attempt_by_id(
            attempt_id=attempt.id,
            learner_id=attempt.learner_id,
        )

        self.assertEqual(found_attempt, attempt)


class TakingQuestionSelectorsTestCase(TestCase):
    """
    Тесты селекторов вопросов и вариантов для прохождения.
    """

    def test_taking_question_list_queryset_returns_active_questions(self) -> None:
        """
        Селектор возвращает только активные вопросы теста.
        """

        exam = create_test()
        active_question = create_question(
            test=exam,
            is_active=True,
            order=1,
        )
        inactive_question = create_question(
            test=exam,
            is_active=False,
            order=2,
        )

        queryset = taking_question_list_queryset(test_id=exam.id)

        self.assertIn(active_question, queryset)
        self.assertNotIn(inactive_question, queryset)

    def test_taking_question_list_queryset_filters_by_test(self) -> None:
        """
        Селектор возвращает вопросы только выбранного теста.
        """

        exam = create_test()
        foreign_exam = create_test()

        question = create_question(test=exam)
        foreign_question = create_question(test=foreign_exam)

        queryset = taking_question_list_queryset(test_id=exam.id)

        self.assertIn(question, queryset)
        self.assertNotIn(foreign_question, queryset)

    def test_taking_option_list_queryset_returns_active_options(self) -> None:
        """
        Селектор возвращает только активные варианты вопроса.
        """

        question = create_question()

        active_option = create_option(
            question=question,
            is_active=True,
            order=1,
        )
        inactive_option = create_option(
            question=question,
            is_active=False,
            order=2,
        )

        queryset = taking_option_list_queryset(question_id=question.id)

        self.assertIn(active_option, queryset)
        self.assertNotIn(inactive_option, queryset)

    def test_taking_options_for_test_queryset_returns_options_for_test(self) -> None:
        """
        Селектор возвращает варианты всех активных вопросов теста.
        """

        exam = create_test()
        foreign_exam = create_test()

        question = create_choice_question_with_options(test=exam)
        foreign_question = create_choice_question_with_options(
            test=foreign_exam,
        )

        option = question.options.first()
        foreign_option = foreign_question.options.first()

        queryset = taking_options_for_test_queryset(test_id=exam.id)

        self.assertIn(option, queryset)
        self.assertNotIn(foreign_option, queryset)

    def test_taking_options_for_test_queryset_ignores_inactive_questions(
        self,
    ) -> None:
        """
        Селектор не возвращает варианты неактивных вопросов.
        """

        exam = create_test()
        question = create_choice_question_with_options(
            test=exam,
            is_active=False,
        )

        option = question.options.first()

        queryset = taking_options_for_test_queryset(test_id=exam.id)

        self.assertNotIn(option, queryset)