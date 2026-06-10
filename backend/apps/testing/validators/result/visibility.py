from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_result_visibility(*, result) -> None:
    """
    Проверяет правила видимости итогового результата.
    """

    errors = {}

    if result.is_visible_to_guardian and not result.is_visible_to_learner:
        errors["is_visible_to_guardian"] = _(
            "Нельзя показать результат родителю, если он скрыт от обучающегося."
        )

    if result.is_visible_to_learner:
        _validate_visible_result_has_grade(
            result=result,
            errors=errors,
        )

    if errors:
        raise ValidationError(errors)


def validate_result_blocking(*, result) -> None:
    """
    Проверяет блокировку повторного прохождения.
    """

    if result.is_blocked and result.attempts_count < 3:
        raise ValidationError(
            {"is_blocked": _("Результат нельзя заблокировать раньше третьей попытки.")}
        )


def _validate_visible_result_has_grade(
    *,
    result,
    errors: dict,
) -> None:
    """
    Проверяет, что видимый результат содержит оценку.
    """

    if result.average_grade is None and result.best_grade is None:
        errors["average_grade"] = _(
            "Перед публикацией результата должна быть рассчитана оценка."
        )
