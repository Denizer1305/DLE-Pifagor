from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_test_attempt_settings(*, test) -> None:
    """
    Проверяет настройки попыток теста.
    """

    errors = {}

    if test.max_attempts < 1:
        errors["max_attempts"] = _("Количество попыток должно быть не меньше 1.")

    if test.max_attempts > 3:
        errors["max_attempts"] = _("В текущей версии доступно не более 3 попыток.")

    if test.time_limit_minutes is not None and test.time_limit_minutes < 1:
        errors["time_limit_minutes"] = _(
            "Ограничение времени должно быть не меньше 1 минуты."
        )

    if errors:
        raise ValidationError(errors)
