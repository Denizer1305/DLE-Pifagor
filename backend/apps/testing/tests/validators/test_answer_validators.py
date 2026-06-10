from __future__ import annotations

from apps.testing.constants import QuestionType
from apps.testing.tests.factories import (
    create_answer,
    create_attempt,
    create_choice_question_with_options,
    create_option,
    create_question,
    create_test,
)
from apps.testing.validators import (
    validate_answer_payload,
    validate_answer_relations,
    validate_answer_scores,
)
from django.core.exceptions import ValidationError
from django.test import TestCase


class TestAnswerPayloadValidatorsTestCase(TestCase):
    """
    Тесты валидаторов payload ответа.
    """

    def test_single_choice_requires_selected_option(self) -> None:
        """
        Ответ с одним вариантом требует selected_option.
        """

        answer = create_answer()
        answer.selected_option = None

        with self.assertRaises(ValidationError):
            validate_answer_payload(answer=answer)

    def test_multiple_choice_requires_selected_options_data(self) -> None:
        """
        Ответ с несколькими вариантами требует список выбранных вариантов.
        """

        question = create_question(
            question_type=QuestionType.MULTIPLE_CHOICE,
        )
        answer = create_answer(
            question=question,
            selected_options_data=[],
        )

        with self.assertRaises(ValidationError):
            validate_answer_payload(answer=answer)

    def test_short_text_requires_text_answer(self) -> None:
        """
        Текстовый вопрос требует текстовый ответ.
        """

        question = create_question(
            question_type=QuestionType.SHORT_TEXT,
        )
        answer = create_answer(
            question=question,
            text_answer="",
        )

        with self.assertRaises(ValidationError):
            validate_answer_payload(answer=answer)

    def test_number_question_requires_number_answer(self) -> None:
        """
        Числовой вопрос требует числовой ответ.
        """

        question = create_question(
            question_type=QuestionType.NUMBER,
            expected_number_answer=4,
        )
        answer = create_answer(
            question=question,
            number_answer=None,
        )

        with self.assertRaises(ValidationError):
            validate_answer_payload(answer=answer)


class TestAnswerRelationValidatorsTestCase(TestCase):
    """
    Тесты валидаторов связей ответа.
    """

    def test_answer_question_must_belong_to_attempt_test(self) -> None:
        """
        Вопрос ответа должен относиться к тесту попытки.
        """

        exam = create_test()
        foreign_exam = create_test()
        attempt = create_attempt(test=exam)
        question = create_choice_question_with_options(test=foreign_exam)

        answer = create_answer(
            attempt=attempt,
            question=question,
        )

        with self.assertRaises(ValidationError):
            validate_answer_relations(answer=answer)

    def test_selected_option_must_belong_to_question(self) -> None:
        """
        Выбранный вариант должен относиться к вопросу ответа.
        """

        question = create_choice_question_with_options()
        foreign_question = create_choice_question_with_options(
            test=question.test,
        )
        foreign_option = create_option(
            question=foreign_question,
            is_correct=True,
        )
        attempt = create_attempt(test=question.test)

        answer = create_answer(
            attempt=attempt,
            question=question,
            selected_option=foreign_option,
        )

        with self.assertRaises(ValidationError):
            validate_answer_relations(answer=answer)


class TestAnswerScoreValidatorsTestCase(TestCase):
    """
    Тесты валидаторов баллов ответа.
    """

    def test_answer_scores_allow_valid_scores(self) -> None:
        """
        Валидатор пропускает корректные баллы.
        """

        question = create_question(score=2)
        answer = create_answer(
            question=question,
            auto_score=1,
            final_score=1,
        )

        validate_answer_scores(answer=answer)

    def test_answer_scores_reject_score_above_question_score(self) -> None:
        """
        Балл ответа не может быть больше балла вопроса.
        """

        question = create_question(score=1)
        answer = create_answer(
            question=question,
            auto_score=2,
        )

        with self.assertRaises(ValidationError):
            validate_answer_scores(answer=answer)
