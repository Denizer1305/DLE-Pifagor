from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_answer_relations(*, answer) -> None:
    """
    Проверяет связи ответа с попыткой, вопросом и вариантом.
    """

    errors = {}

    if answer.question.test_id != answer.attempt.test_id:
        errors["question"] = _("Вопрос должен относиться к тесту текущей попытки.")

    if answer.selected_option_id:
        if answer.selected_option.question_id != answer.question_id:
            errors["selected_option"] = _(
                "Выбранный вариант должен относиться к текущему вопросу."
            )

    if errors:
        raise ValidationError(errors)


def validate_answer_scores(*, answer) -> None:
    """
    Проверяет баллы ответа.
    """

    max_score = answer.question.score
    errors = {}

    _validate_score_value(
        errors=errors,
        field_name="auto_score",
        value=answer.auto_score,
        max_score=max_score,
    )
    _validate_score_value(
        errors=errors,
        field_name="teacher_score",
        value=answer.teacher_score,
        max_score=max_score,
        allow_null=True,
    )
    _validate_score_value(
        errors=errors,
        field_name="final_score",
        value=answer.final_score,
        max_score=max_score,
        allow_null=True,
    )

    if errors:
        raise ValidationError(errors)


def _validate_score_value(
    *,
    errors: dict,
    field_name: str,
    value,
    max_score,
    allow_null: bool = False,
) -> None:
    """
    Проверяет одно значение балла.
    """

    if value is None:
        if allow_null:
            return

        errors[field_name] = _("Балл не может быть пустым.")
        return

    if value < 0:
        errors[field_name] = _("Балл не может быть отрицательным.")

    if value > max_score:
        errors[field_name] = _("Балл не может быть больше балла за вопрос.")
