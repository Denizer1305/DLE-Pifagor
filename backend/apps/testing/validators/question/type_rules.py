from __future__ import annotations

from apps.testing.constants import QuestionCheckMode, QuestionType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_question_type_rules(*, question) -> None:
    """
    Проверяет согласованность типа вопроса и режима проверки.
    """

    errors = {}

    if question.question_type == QuestionType.SHORT_TEXT:
        if question.check_mode == QuestionCheckMode.AUTO:
            errors["check_mode"] = _(
                "Короткий текстовый ответ нельзя проверять строго автоматически."
            )

    auto_question_types = {
        QuestionType.SINGLE_CHOICE,
        QuestionType.MULTIPLE_CHOICE,
        QuestionType.TRUE_FALSE,
        QuestionType.NUMBER,
    }

    if question.question_type in auto_question_types:
        if question.check_mode == QuestionCheckMode.MANUAL:
            errors["check_mode"] = _(
                "Для этого типа вопроса используйте автоматическую "
                "или полуавтоматическую проверку."
            )

    if errors:
        raise ValidationError(errors)


def validate_question_expected_answers(*, question) -> None:
    """
    Проверяет поля ожидаемых ответов.
    """

    errors = {}

    if question.question_type == QuestionType.NUMBER:
        if question.expected_number_answer is None:
            errors["expected_number_answer"] = _(
                "Для числового вопроса укажите ожидаемый ответ."
            )

    if question.question_type != QuestionType.NUMBER:
        if question.expected_number_answer is not None:
            errors["expected_number_answer"] = _(
                "Числовой ожидаемый ответ допустим только для числового вопроса."
            )

    if question.question_type != QuestionType.SHORT_TEXT:
        if question.expected_text_answer:
            errors["expected_text_answer"] = _(
                "Текстовый ожидаемый ответ допустим только для текстового вопроса."
            )

    if errors:
        raise ValidationError(errors)
