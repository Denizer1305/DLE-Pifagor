from __future__ import annotations

from apps.testing.constants import TestAttemptStatus, TestStatus
from apps.testing.services import (
    cancel_test_attempt,
    save_attempt_answer,
    save_attempt_answers,
    start_test_attempt,
    submit_test_attempt,
)
from apps.testing.tests.factories import (
    create_attempt,
    create_choice_question_with_options,
    create_learner,
    create_test,
)
from django.core.exceptions import ValidationError
from django.test import TestCase


class TestAttemptServicesTestCase(TestCase):
    """
    Тесты сервисов попыток прохождения теста.
    """

    def test_start_test_attempt_creates_attempt(self) -> None:
        """
        Сервис создаёт первую попытку прохождения теста.
        """

        exam = create_test(
            status=TestStatus.PUBLISHED,
            is_active=True,
        )
        learner = create_learner()

        attempt = start_test_attempt(
            test=exam,
            learner=learner,
        )

        self.assertEqual(attempt.test, exam)
        self.assertEqual(attempt.learner, learner)
        self.assertEqual(attempt.attempt_number, 1)
        self.assertEqual(attempt.status, TestAttemptStatus.STARTED)

    def test_start_test_attempt_rejects_unpublished_test(self) -> None:
        """
        Нельзя начать попытку неопубликованного теста.
        """

        exam = create_test(status=TestStatus.DRAFT)
        learner = create_learner()

        with self.assertRaises(ValidationError):
            start_test_attempt(
                test=exam,
                learner=learner,
            )

    def test_submit_test_attempt_sets_submitted_status(self) -> None:
        """
        Сервис отправляет попытку на проверку.
        """

        attempt = create_attempt(status=TestAttemptStatus.STARTED)

        submitted_attempt = submit_test_attempt(attempt=attempt)

        self.assertEqual(
            submitted_attempt.status,
            TestAttemptStatus.SUBMITTED,
        )
        self.assertIsNotNone(submitted_attempt.submitted_at)

    def test_cancel_test_attempt_sets_cancelled_status(self) -> None:
        """
        Сервис отменяет попытку.
        """

        attempt = create_attempt(status=TestAttemptStatus.STARTED)

        cancelled_attempt = cancel_test_attempt(attempt=attempt)

        self.assertEqual(
            cancelled_attempt.status,
            TestAttemptStatus.CANCELLED,
        )

    def test_save_attempt_answer_creates_answer(self) -> None:
        """
        Сервис сохраняет один ответ попытки.
        """

        attempt = create_attempt(status=TestAttemptStatus.STARTED)
        question = create_choice_question_with_options(test=attempt.test)
        option = question.options.filter(is_correct=True).first()

        answer = save_attempt_answer(
            attempt=attempt,
            data={
                "question_id": question.id,
                "selected_option_id": option.id,
            },
        )

        self.assertEqual(answer.attempt, attempt)
        self.assertEqual(answer.question, question)
        self.assertEqual(answer.selected_option, option)

    def test_save_attempt_answers_creates_many_answers(self) -> None:
        """
        Сервис сохраняет набор ответов попытки.
        """

        attempt = create_attempt(status=TestAttemptStatus.STARTED)
        first_question = create_choice_question_with_options(
            test=attempt.test,
        )
        second_question = create_choice_question_with_options(
            test=attempt.test,
        )

        first_option = first_question.options.filter(is_correct=True).first()
        second_option = second_question.options.filter(is_correct=True).first()

        answers = save_attempt_answers(
            attempt=attempt,
            answers_data=[
                {
                    "question_id": first_question.id,
                    "selected_option_id": first_option.id,
                },
                {
                    "question_id": second_question.id,
                    "selected_option_id": second_option.id,
                },
            ],
        )

        self.assertEqual(len(answers), 2)
        self.assertEqual(attempt.answers.count(), 2)
