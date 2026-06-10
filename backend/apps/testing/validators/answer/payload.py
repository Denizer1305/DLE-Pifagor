from __future__ import annotations

from apps.testing.constants import QuestionType
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_answer_payload(*, answer) -> None:
    """
    Проверяет, что ответ соответствует типу вопроса.
    """

    question_type = answer.question.question_type

    if question_type == QuestionType.SINGLE_CHOICE:
        _validate_single_choice_answer(answer=answer)

    if question_type == QuestionType.MULTIPLE_CHOICE:
        _validate_multiple_choice_answer(answer=answer)

    if question_type == QuestionType.TRUE_FALSE:
        _validate_true_false_answer(answer=answer)

    if question_type == QuestionType.SHORT_TEXT:
        _validate_short_text_answer(answer=answer)

    if question_type == QuestionType.NUMBER:
        _validate_number_answer(answer=answer)


def _validate_single_choice_answer(*, answer) -> None:
    """
    Проверяет ответ с одним вариантом.
    """

    if not answer.selected_option_id:
        raise ValidationError({"selected_option": _("Выберите один вариант ответа.")})


def _validate_multiple_choice_answer(*, answer) -> None:
    """
    Проверяет ответ с несколькими вариантами.
    """

    if not answer.selected_options_data:
        raise ValidationError(
            {"selected_options_data": _("Выберите хотя бы один вариант ответа.")}
        )

    if not isinstance(answer.selected_options_data, list):
        raise ValidationError(
            {"selected_options_data": _("Выбранные варианты должны быть списком.")}
        )


def _validate_true_false_answer(*, answer) -> None:
    """
    Проверяет ответ верно/неверно.
    """

    if not answer.selected_option_id:
        raise ValidationError({"selected_option": _("Выберите вариант верно/неверно.")})


def _validate_short_text_answer(*, answer) -> None:
    """
    Проверяет короткий текстовый ответ.
    """

    if not answer.text_answer.strip():
        raise ValidationError({"text_answer": _("Введите текстовый ответ.")})


def _validate_number_answer(*, answer) -> None:
    """
    Проверяет числовой ответ.
    """

    if answer.number_answer is None:
        raise ValidationError({"number_answer": _("Введите числовой ответ.")})
