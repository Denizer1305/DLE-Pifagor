from __future__ import annotations

from apps.testing.models import Test as ExamModel
from apps.testing.models import TestAttempt as AttemptModel
from apps.testing.models import TestAttemptAnswer as AnswerModel
from apps.testing.models import TestLearnerResult as LearnerResultModel
from apps.testing.models import TestQuestion as QuestionModel
from apps.testing.models import TestQuestionOption as OptionModel
from apps.testing.tests.factories import (
    create_answer,
    create_attempt,
    create_choice_question_with_options,
    create_option,
    create_question,
    create_result,
    create_test,
)
from django.test import TestCase


class TestingModelsTestCase(TestCase):
    """
    Smoke-тесты моделей модуля тестирования.
    """

    def test_create_test(self) -> None:
        """
        Учебный тест создаётся корректно.
        """

        test = create_test(title="Контрольный тест")

        self.assertIsInstance(test, ExamModel)
        self.assertEqual(test.title, "Контрольный тест")
        self.assertEqual(str(test), "Контрольный тест")

    def test_create_question(self) -> None:
        """
        Вопрос теста создаётся корректно.
        """

        test = create_test()
        question = create_question(
            test=test,
            text="Сколько будет 2 + 2?",
        )

        self.assertIsInstance(question, QuestionModel)
        self.assertEqual(question.test, test)
        self.assertEqual(question.text, "Сколько будет 2 + 2?")
        self.assertEqual(str(question), question.title)

    def test_create_question_option(self) -> None:
        """
        Вариант ответа создаётся корректно.
        """

        question = create_question()
        option = create_option(
            question=question,
            text="4",
            is_correct=True,
        )

        self.assertIsInstance(option, OptionModel)
        self.assertEqual(option.question, question)
        self.assertEqual(option.text, "4")
        self.assertTrue(option.is_correct)
        self.assertEqual(str(option), "4")

    def test_create_choice_question_with_options(self) -> None:
        """
        Фабрика создаёт вопрос с двумя вариантами ответа.
        """

        question = create_choice_question_with_options()

        self.assertEqual(question.options.count(), 2)
        self.assertEqual(
            question.options.filter(is_correct=True).count(),
            1,
        )

    def test_create_attempt(self) -> None:
        """
        Попытка прохождения теста создаётся корректно.
        """

        test = create_test()
        attempt = create_attempt(test=test)

        self.assertIsInstance(attempt, AttemptModel)
        self.assertEqual(attempt.test, test)
        self.assertEqual(attempt.attempt_number, 1)
        self.assertIn("попытка", str(attempt))

    def test_create_answer(self) -> None:
        """
        Ответ на вопрос теста создаётся корректно.
        """

        attempt = create_attempt()
        question = create_choice_question_with_options(
            test=attempt.test,
        )
        selected_option = question.options.filter(
            is_correct=True,
        ).first()

        answer = create_answer(
            attempt=attempt,
            question=question,
            selected_option=selected_option,
        )

        self.assertIsInstance(answer, AnswerModel)
        self.assertEqual(answer.attempt, attempt)
        self.assertEqual(answer.question, question)
        self.assertEqual(answer.selected_option, selected_option)
        self.assertIn(str(attempt), str(answer))

    def test_create_result(self) -> None:
        """
        Итоговый результат теста создаётся корректно.
        """

        attempt = create_attempt()
        result = create_result(
            test=attempt.test,
            learner=attempt.learner,
            last_attempt=attempt,
        )

        self.assertIsInstance(result, LearnerResultModel)
        self.assertEqual(result.test, attempt.test)
        self.assertEqual(result.learner, attempt.learner)
        self.assertEqual(result.last_attempt, attempt)
        self.assertIn(str(attempt.test), str(result))

    def test_model_full_clean_for_valid_objects(self) -> None:
        """
        Валидные объекты проходят model full_clean.
        """

        test = create_test()
        question = create_choice_question_with_options(test=test)
        option = question.options.filter(is_correct=True).first()
        attempt = create_attempt(test=test)
        answer = create_answer(
            attempt=attempt,
            question=question,
            selected_option=option,
        )
        result = create_result(
            test=test,
            learner=attempt.learner,
            last_attempt=attempt,
        )

        test.full_clean()
        question.full_clean()
        option.full_clean()
        attempt.full_clean()
        answer.full_clean()
        result.full_clean()
