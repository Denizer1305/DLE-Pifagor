from __future__ import annotations

from apps.testing.constants import QuestionType
from apps.testing.services import (
    create_question,
    create_question_option,
    reorder_question_options,
    reorder_questions,
    update_question,
    update_question_option,
)
from apps.testing.tests.factories import create_option
from apps.testing.tests.factories import create_question as create_question_factory
from apps.testing.tests.factories import create_test
from django.test import TestCase


class TestQuestionServicesTestCase(TestCase):
    """
    Тесты сервисов вопросов теста.
    """

    def test_create_question_creates_question(self) -> None:
        """
        Сервис создаёт вопрос теста.
        """

        exam = create_test()

        question = create_question(
            data={
                "test": exam,
                "question_type": QuestionType.SINGLE_CHOICE,
                "title": "Вопрос 1",
                "text": "Сколько будет 2 + 2?",
                "order": 1,
                "score": 1,
            }
        )

        self.assertEqual(question.test, exam)
        self.assertEqual(question.title, "Вопрос 1")
        self.assertEqual(question.order, 1)

    def test_update_question_updates_text(self) -> None:
        """
        Сервис обновляет вопрос.
        """

        question = create_question_factory(text="Старый текст")

        updated_question = update_question(
            question=question,
            data={
                "text": "Новый текст",
            },
        )

        self.assertEqual(updated_question.text, "Новый текст")

    def test_create_question_option_creates_option(self) -> None:
        """
        Сервис создаёт вариант ответа.
        """

        question = create_question_factory()

        option = create_question_option(
            data={
                "question": question,
                "text": "Ответ",
                "order": 1,
                "is_correct": True,
                "score": 1,
            }
        )

        self.assertEqual(option.question, question)
        self.assertEqual(option.text, "Ответ")
        self.assertTrue(option.is_correct)

    def test_update_question_option_updates_text(self) -> None:
        """
        Сервис обновляет вариант ответа.
        """

        option = create_option(text="Старый ответ")

        updated_option = update_question_option(
            option=option,
            data={
                "text": "Новый ответ",
            },
        )

        self.assertEqual(updated_option.text, "Новый ответ")

    def test_reorder_questions_updates_order(self) -> None:
        """
        Сервис безопасно переупорядочивает вопросы.
        """

        exam = create_test()
        first_question = create_question_factory(test=exam, order=1)
        second_question = create_question_factory(test=exam, order=2)

        reorder_questions(
            test_id=exam.id,
            ordered_question_ids=[
                second_question.id,
                first_question.id,
            ],
        )

        first_question.refresh_from_db()
        second_question.refresh_from_db()

        self.assertEqual(second_question.order, 1)
        self.assertEqual(first_question.order, 2)

    def test_reorder_question_options_updates_order(self) -> None:
        """
        Сервис безопасно переупорядочивает варианты ответа.
        """

        question = create_question_factory()
        first_option = create_option(question=question, order=1)
        second_option = create_option(question=question, order=2)

        reorder_question_options(
            question_id=question.id,
            ordered_option_ids=[
                second_option.id,
                first_option.id,
            ],
        )

        first_option.refresh_from_db()
        second_option.refresh_from_db()

        self.assertEqual(second_option.order, 1)
        self.assertEqual(first_option.order, 2)
