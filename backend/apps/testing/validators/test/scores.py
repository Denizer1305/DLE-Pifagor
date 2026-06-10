from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_test_scores(*, test) -> None:
    """
    Проверяет настройки баллов теста.
    """

    errors = {}

    if test.max_score < 1:
        errors["max_score"] = _("Максимальный балл должен быть не меньше 1.")

    if test.passing_score < 0:
        errors["passing_score"] = _("Проходной балл не может быть отрицательным.")

    if test.passing_score > test.max_score:
        errors["passing_score"] = _(
            "Проходной балл не может быть больше максимального."
        )

    if errors:
        raise ValidationError(errors)
