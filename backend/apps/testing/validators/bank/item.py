from __future__ import annotations

from apps.testing.constants import QuestionCheckMode, QuestionType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_bank_item(item) -> None:
    """
    Валидирует шаблон вопроса банка тестовых заданий.
    """

    validate_bank_item_score(item=item)
    validate_bank_item_tags(item=item)
    validate_bank_item_type_rules(item=item)
    validate_bank_item_expected_answers(item=item)


def validate_bank_item_score(item) -> None:
    """
    Проверяет балл шаблона вопроса.
    """

    if item.score <= 0:
        raise ValidationError(
            {"score": _("Балл за шаблон вопроса должен быть больше нуля.")}
        )


def validate_bank_item_tags(item) -> None:
    """
    Проверяет формат тегов шаблона вопроса.
    """

    if item.tags_data in (None, ""):
        return

    if not isinstance(item.tags_data, list):
        raise ValidationError({"tags_data": _("Теги должны храниться списком.")})

    invalid_tags = [
        tag for tag in item.tags_data if not isinstance(tag, str) or not tag.strip()
    ]

    if invalid_tags:
        raise ValidationError(
            {"tags_data": _("Каждый тег должен быть непустой строкой.")}
        )


def validate_bank_item_type_rules(item) -> None:
    """
    Проверяет правила типа вопроса и режима проверки.
    """

    if (
        item.question_type == QuestionType.SHORT_TEXT
        and item.check_mode == QuestionCheckMode.AUTO
    ):
        raise ValidationError(
            {
                "check_mode": _(
                    "Короткий текстовый ответ нельзя проверять " "строго автоматически."
                )
            }
        )

    if (
        item.question_type
        in {
            QuestionType.SINGLE_CHOICE,
            QuestionType.MULTIPLE_CHOICE,
            QuestionType.TRUE_FALSE,
        }
        and item.check_mode == QuestionCheckMode.MANUAL
    ):
        return


def validate_bank_item_expected_answers(item) -> None:
    """
    Проверяет ожидаемые ответы шаблона вопроса.
    """

    if item.question_type == QuestionType.NUMBER:
        _validate_number_expected_answer(item=item)
        return

    if item.question_type == QuestionType.SHORT_TEXT:
        _validate_text_expected_answer(item=item)
        return

    _validate_choice_question_expected_answers(item=item)


def _validate_number_expected_answer(item) -> None:
    """
    Проверяет ожидаемый ответ для числового вопроса.
    """

    if item.expected_number_answer is None:
        raise ValidationError(
            {
                "expected_number_answer": _(
                    "Для числового вопроса укажите ожидаемый числовой ответ."
                )
            }
        )

    if item.expected_text_answer:
        raise ValidationError(
            {
                "expected_text_answer": _(
                    "Для числового вопроса нельзя указывать текстовый ответ."
                )
            }
        )


def _validate_text_expected_answer(item) -> None:
    """
    Проверяет ожидаемый ответ для короткого текстового вопроса.
    """

    if item.check_mode == QuestionCheckMode.SEMI_AUTO:
        if not item.expected_text_answer:
            raise ValidationError(
                {
                    "expected_text_answer": _(
                        "Для полуавтоматической проверки укажите "
                        "ожидаемый текстовый ответ."
                    )
                }
            )

    if item.expected_number_answer is not None:
        raise ValidationError(
            {
                "expected_number_answer": _(
                    "Для текстового вопроса нельзя указывать числовой ответ."
                )
            }
        )


def _validate_choice_question_expected_answers(item) -> None:
    """
    Проверяет, что у вопроса с вариантами нет expected answer полей.
    """

    errors = {}

    if item.expected_text_answer:
        errors["expected_text_answer"] = _(
            "Для вопроса с вариантами ответа нельзя указывать "
            "ожидаемый текстовый ответ."
        )

    if item.expected_number_answer is not None:
        errors["expected_number_answer"] = _(
            "Для вопроса с вариантами ответа нельзя указывать "
            "ожидаемый числовой ответ."
        )

    if errors:
        raise ValidationError(errors)
