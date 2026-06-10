from __future__ import annotations

from apps.testing.constants import QuestionCheckMode, QuestionType
from apps.testing.tests.factories import (
    create_choice_question_with_options,
    create_option,
    create_question,
)
from apps.testing.validators import (
    validate_question_expected_answers,
    validate_question_options_for_publish,
    validate_question_score,
    validate_question_type_rules,
)
from django.core.exceptions import ValidationError
from django.test import TestCase


class TestQuestionTypeValidatorsTestCase(TestCase):
    """
    Тесты валидаторов типа вопроса.
    """

    def test_short_text_cannot_be_strict_auto_checked(self) -> None:
        """
        Короткий текстовый ответ нельзя проверять строго автоматически.
        """

        question = create_question(
            question_type=QuestionType.SHORT_TEXT,
            check_mode=QuestionCheckMode.AUTO,
        )

        with self.assertRaises(ValidationError):
            validate_question_type_rules(question=question)

    def test_number_question_requires_expected_number_answer(self) -> None:
        """
        Числовой вопрос требует ожидаемый числовой ответ.
        """

        question = create_question(
            question_type=QuestionType.NUMBER,
            expected_number_answer=None,
        )

        with self.assertRaises(ValidationError):
            validate_question_expected_answers(question=question)

    def test_number_question_allows_expected_number_answer(self) -> None:
        """
        Числовой вопрос пропускается при наличии ожидаемого ответа.
        """

        question = create_question(
            question_type=QuestionType.NUMBER,
            expected_number_answer=4,
        )

        validate_question_expected_answers(question=question)

    def test_non_text_question_rejects_expected_text_answer(self) -> None:
        """
        Ожидаемый текстовый ответ нельзя указывать не для текстового вопроса.
        """

        question = create_question(
            question_type=QuestionType.SINGLE_CHOICE,
            expected_text_answer="ответ",
        )

        with self.assertRaises(ValidationError):
            validate_question_expected_answers(question=question)


class TestQuestionScoreValidatorsTestCase(TestCase):
    """
    Тесты валидаторов баллов вопроса.
    """

    def test_validate_question_score_allows_positive_score(self) -> None:
        """
        Валидатор пропускает положительный балл.
        """

        question = create_question(score=1)

        validate_question_score(question=question)

    def test_validate_question_score_rejects_zero_score(self) -> None:
        """
        Валидатор запрещает нулевой балл.
        """

        question = create_question(score=0)

        with self.assertRaises(ValidationError):
            validate_question_score(question=question)


class TestQuestionOptionValidatorsTestCase(TestCase):
    """
    Тесты валидаторов вариантов ответа.
    """

    def test_single_choice_requires_one_correct_option(self) -> None:
        """
        Вопрос с одним ответом требует ровно один правильный вариант.
        """

        question = create_question(
            question_type=QuestionType.SINGLE_CHOICE,
        )
        create_option(question=question, is_correct=False)
        create_option(question=question, is_correct=False)

        with self.assertRaises(ValidationError):
            validate_question_options_for_publish(question=question)

    def test_single_choice_allows_one_correct_option(self) -> None:
        """
        Вопрос с одним ответом пропускается с одним правильным вариантом.
        """

        question = create_choice_question_with_options(
            question_type=QuestionType.SINGLE_CHOICE,
        )

        validate_question_options_for_publish(question=question)

    def test_multiple_choice_requires_at_least_one_correct_option(self) -> None:
        """
        Вопрос с несколькими ответами требует хотя бы один правильный вариант.
        """

        question = create_question(
            question_type=QuestionType.MULTIPLE_CHOICE,
        )
        create_option(question=question, is_correct=False)
        create_option(question=question, is_correct=False)

        with self.assertRaises(ValidationError):
            validate_question_options_for_publish(question=question)

    def test_true_false_requires_two_options(self) -> None:
        """
        Вопрос верно/неверно требует ровно два варианта.
        """

        question = create_question(
            question_type=QuestionType.TRUE_FALSE,
        )
        create_option(question=question, is_correct=True)

        with self.assertRaises(ValidationError):
            validate_question_options_for_publish(question=question)
