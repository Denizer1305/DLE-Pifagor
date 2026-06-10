from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_result_attempt_counters(*, result) -> None:
    """
    Проверяет счётчики попыток итогового результата.
    """

    errors = {}

    if result.attempts_count < 0:
        errors["attempts_count"] = _("Количество попыток не может быть отрицательным.")

    if result.confirmed_attempts_count < 0:
        errors["confirmed_attempts_count"] = _(
            "Количество подтверждённых попыток не может быть отрицательным."
        )

    if result.confirmed_attempts_count > result.attempts_count:
        errors["confirmed_attempts_count"] = _(
            "Подтверждённых попыток не может быть больше общего количества."
        )

    if errors:
        raise ValidationError(errors)


def validate_result_scores(*, result) -> None:
    """
    Проверяет агрегированные баллы и оценки.
    """

    errors = {}

    _validate_non_negative_value(
        errors=errors,
        field_name="average_score",
        value=result.average_score,
    )
    _validate_non_negative_value(
        errors=errors,
        field_name="best_score",
        value=result.best_score,
    )

    _validate_grade_value(
        errors=errors,
        field_name="average_grade",
        value=result.average_grade,
    )
    _validate_grade_value(
        errors=errors,
        field_name="best_grade",
        value=result.best_grade,
    )

    if errors:
        raise ValidationError(errors)


def _validate_non_negative_value(
    *,
    errors: dict,
    field_name: str,
    value,
) -> None:
    """
    Проверяет, что числовое значение не отрицательное.
    """

    if value is not None and value < 0:
        errors[field_name] = _("Значение не может быть отрицательным.")


def _validate_grade_value(
    *,
    errors: dict,
    field_name: str,
    value,
) -> None:
    """
    Проверяет значение оценки.
    """

    if value is None:
        return

    if value < 2 or value > 5:
        errors[field_name] = _("Оценка должна быть в диапазоне от 2 до 5.")
