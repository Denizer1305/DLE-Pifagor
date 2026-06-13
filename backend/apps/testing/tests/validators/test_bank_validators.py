from __future__ import annotations

from apps.testing.constants import BankItemStatus, QuestionCheckMode, QuestionType
from apps.testing.tests.factories import (
    create_bank_item,
    create_bank_item_with_options,
    create_bank_option,
)
from apps.testing.validators import (
    validate_bank_item,
    validate_bank_item_can_be_archived,
    validate_bank_item_can_be_published,
    validate_bank_item_can_be_restored,
    validate_bank_option,
)
from django.core.exceptions import ValidationError
from django.test import TestCase


class QuestionBankItemValidatorsTestCase(TestCase):
    """
    Тесты валидаторов шаблонов вопросов банка заданий.
    """

    def test_validate_bank_item_allows_valid_choice_item(self) -> None:
        """
        Валидный шаблон вопроса проходит проверку.
        """

        bank_item = create_bank_item()

        validate_bank_item(item=bank_item)

    def test_validate_bank_item_rejects_zero_score(self) -> None:
        """
        Шаблон вопроса не может иметь нулевой балл.
        """

        bank_item = create_bank_item()
        bank_item.score = 0

        with self.assertRaises(ValidationError):
            validate_bank_item(item=bank_item)

    def test_validate_bank_item_rejects_invalid_tags_type(self) -> None:
        """
        Теги должны храниться списком.
        """

        bank_item = create_bank_item()
        bank_item.tags_data = "math"

        with self.assertRaises(ValidationError):
            validate_bank_item(item=bank_item)

    def test_validate_bank_item_rejects_empty_tag(self) -> None:
        """
        Каждый тег должен быть непустой строкой.
        """

        bank_item = create_bank_item()
        bank_item.tags_data = ["математика", ""]

        with self.assertRaises(ValidationError):
            validate_bank_item(item=bank_item)

    def test_short_text_cannot_be_strict_auto_checked(self) -> None:
        """
        Короткий текстовый ответ нельзя проверять строго автоматически.
        """

        bank_item = create_bank_item(
            question_type=QuestionType.SHORT_TEXT,
            check_mode=QuestionCheckMode.AUTO,
        )

        with self.assertRaises(ValidationError):
            validate_bank_item(item=bank_item)

    def test_number_question_requires_expected_number_answer(self) -> None:
        """
        Числовой шаблон требует ожидаемый числовой ответ.
        """

        bank_item = create_bank_item(
            question_type=QuestionType.NUMBER,
            expected_number_answer=None,
        )

        with self.assertRaises(ValidationError):
            validate_bank_item(item=bank_item)

    def test_number_question_allows_expected_number_answer(self) -> None:
        """
        Числовой шаблон проходит проверку с ожидаемым числовым ответом.
        """

        bank_item = create_bank_item(
            question_type=QuestionType.NUMBER,
            expected_number_answer=4,
        )

        validate_bank_item(item=bank_item)


class QuestionBankOptionValidatorsTestCase(TestCase):
    """
    Тесты валидаторов вариантов ответа банка заданий.
    """

    def test_validate_bank_option_allows_valid_option(self) -> None:
        """
        Валидный вариант ответа проходит проверку.
        """

        bank_item = create_bank_item(score=2)
        option = create_bank_option(
            bank_item=bank_item,
            score=1,
        )

        validate_bank_option(option=option)

    def test_validate_bank_option_rejects_negative_score(self) -> None:
        """
        Балл варианта не может быть отрицательным.
        """

        option = create_bank_option()
        option.score = -1

        with self.assertRaises(ValidationError):
            validate_bank_option(option=option)

    def test_validate_bank_option_rejects_score_above_item_score(self) -> None:
        """
        Балл варианта не может быть больше балла шаблона.
        """

        bank_item = create_bank_item(score=1)
        option = create_bank_option(
            bank_item=bank_item,
            score=2,
        )

        with self.assertRaises(ValidationError):
            validate_bank_option(option=option)


class QuestionBankPublicationValidatorsTestCase(TestCase):
    """
    Тесты валидаторов публикации шаблонов вопросов.
    """

    def test_published_choice_item_requires_options(self) -> None:
        """
        Шаблон с вариантами нельзя опубликовать без вариантов ответа.
        """

        bank_item = create_bank_item(
            question_type=QuestionType.SINGLE_CHOICE,
        )

        with self.assertRaises(ValidationError):
            validate_bank_item_can_be_published(item=bank_item)

    def test_single_choice_item_can_be_published_with_one_correct_option(self) -> None:
        """
        Шаблон с одним правильным вариантом можно опубликовать.
        """

        bank_item = create_bank_item_with_options(
            question_type=QuestionType.SINGLE_CHOICE,
        )

        validate_bank_item_can_be_published(item=bank_item)

    def test_archived_item_cannot_be_published(self) -> None:
        """
        Архивный шаблон нельзя опубликовать.
        """

        bank_item = create_bank_item_with_options(
            status=BankItemStatus.ARCHIVED,
        )

        with self.assertRaises(ValidationError):
            validate_bank_item_can_be_published(item=bank_item)

    def test_draft_item_can_be_archived(self) -> None:
        """
        Черновой шаблон можно архивировать.
        """

        bank_item = create_bank_item(status=BankItemStatus.DRAFT)

        validate_bank_item_can_be_archived(item=bank_item)

    def test_archived_item_cannot_be_archived_again(self) -> None:
        """
        Архивный шаблон нельзя архивировать повторно.
        """

        bank_item = create_bank_item(status=BankItemStatus.ARCHIVED)

        with self.assertRaises(ValidationError):
            validate_bank_item_can_be_archived(item=bank_item)

    def test_archived_item_can_be_restored(self) -> None:
        """
        Архивный шаблон можно восстановить.
        """

        bank_item = create_bank_item(status=BankItemStatus.ARCHIVED)

        validate_bank_item_can_be_restored(item=bank_item)

    def test_draft_item_cannot_be_restored(self) -> None:
        """
        Восстановить можно только архивный шаблон.
        """

        bank_item = create_bank_item(status=BankItemStatus.DRAFT)

        with self.assertRaises(ValidationError):
            validate_bank_item_can_be_restored(item=bank_item)
