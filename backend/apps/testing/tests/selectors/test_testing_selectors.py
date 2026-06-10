from __future__ import annotations

from apps.testing.constants import TestAttemptStatus as AttemptStatus
from apps.testing.constants import TestStatus as ExamStatus
from apps.testing.selectors import (
    answer_list_queryset,
    attempt_list_queryset,
    option_list_queryset,
    question_list_queryset,
    result_list_queryset,
)
from apps.testing.selectors import test_list_queryset as exam_list_queryset
from apps.testing.tests.factories import (
    create_answer,
    create_attempt,
    create_choice_question_with_options,
    create_option,
    create_question,
    create_result,
    create_test,
    create_visible_result,
)
from django.test import TestCase


class TestingSelectorsTestCase(TestCase):
    """
    Тесты селекторов модуля testing.
    """

    def test_test_list_queryset_filters_by_status(self) -> None:
        """
        Селектор тестов фильтрует по статусу.
        """

        published_exam = create_test(status=ExamStatus.PUBLISHED)
        draft_exam = create_test(status=ExamStatus.DRAFT)

        queryset = exam_list_queryset(status=ExamStatus.PUBLISHED)

        self.assertIn(published_exam, queryset)
        self.assertNotIn(draft_exam, queryset)

    def test_test_list_queryset_filters_by_teacher(self) -> None:
        """
        Селектор тестов фильтрует по преподавателю-владельцу.
        """

        first_exam = create_test()
        second_exam = create_test()

        queryset = exam_list_queryset(
            owner_teacher_id=first_exam.owner_teacher_id,
        )

        self.assertIn(first_exam, queryset)
        self.assertNotIn(second_exam, queryset)

    def test_question_list_queryset_filters_by_test(self) -> None:
        """
        Селектор вопросов фильтрует по тесту.
        """

        exam = create_test()
        foreign_exam = create_test()

        question = create_question(test=exam)
        foreign_question = create_question(test=foreign_exam)

        queryset = question_list_queryset(test_id=exam.id)

        self.assertIn(question, queryset)
        self.assertNotIn(foreign_question, queryset)

    def test_option_list_queryset_filters_by_question(self) -> None:
        """
        Селектор вариантов ответа фильтрует по вопросу.
        """

        question = create_question()
        foreign_question = create_question()

        option = create_option(question=question)
        foreign_option = create_option(question=foreign_question)

        queryset = option_list_queryset(question_id=question.id)

        self.assertIn(option, queryset)
        self.assertNotIn(foreign_option, queryset)

    def test_attempt_list_queryset_filters_by_learner(self) -> None:
        """
        Селектор попыток фильтрует по обучающемуся.
        """

        attempt = create_attempt()
        foreign_attempt = create_attempt()

        queryset = attempt_list_queryset(
            learner_id=attempt.learner_id,
        )

        self.assertIn(attempt, queryset)
        self.assertNotIn(foreign_attempt, queryset)

    def test_attempt_list_queryset_filters_by_status(self) -> None:
        """
        Селектор попыток фильтрует по статусу.
        """

        submitted_attempt = create_attempt(status=AttemptStatus.SUBMITTED)
        started_attempt = create_attempt(status=AttemptStatus.STARTED)

        queryset = attempt_list_queryset(status=AttemptStatus.SUBMITTED)

        self.assertIn(submitted_attempt, queryset)
        self.assertNotIn(started_attempt, queryset)

    def test_answer_list_queryset_filters_by_attempt(self) -> None:
        """
        Селектор ответов фильтрует по попытке.
        """

        attempt = create_attempt()
        foreign_attempt = create_attempt()

        question = create_choice_question_with_options(test=attempt.test)
        foreign_question = create_choice_question_with_options(
            test=foreign_attempt.test,
        )

        answer = create_answer(
            attempt=attempt,
            question=question,
        )
        foreign_answer = create_answer(
            attempt=foreign_attempt,
            question=foreign_question,
        )

        queryset = answer_list_queryset(attempt_id=attempt.id)

        self.assertIn(answer, queryset)
        self.assertNotIn(foreign_answer, queryset)

    def test_result_list_queryset_filters_by_learner(self) -> None:
        """
        Селектор результатов фильтрует по обучающемуся.
        """

        result = create_result()
        foreign_result = create_result()

        queryset = result_list_queryset(
            learner_id=result.learner_id,
        )

        self.assertIn(result, queryset)
        self.assertNotIn(foreign_result, queryset)

    def test_result_list_queryset_filters_by_visibility(self) -> None:
        """
        Селектор результатов фильтрует по видимости.
        """

        visible_result = create_visible_result()
        hidden_result = create_result(
            is_visible_to_learner=False,
            is_visible_to_guardian=False,
        )

        queryset = result_list_queryset(is_visible_to_learner=True)

        self.assertIn(visible_result, queryset)
        self.assertNotIn(hidden_result, queryset)
