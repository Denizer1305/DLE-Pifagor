from __future__ import annotations

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

PHONE_PATTERN = re.compile(r"^\+?[1-9]\d{7,14}$")
"""Паттерн международного телефонного номера."""


def normalize_phone_number(value: str) -> str:
    """
    Нормализует номер телефона для проверки.
    """

    return value.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")


def validate_phone_number(value: str) -> None:
    """
    Проверяет номер телефона в международном формате.

    Допускает:
    - цифры;
    - необязательный символ + в начале;
    - длину от 8 до 15 цифр.
    """

    if not value:
        raise ValidationError(_("Номер телефона обязателен."))

    normalized_value = normalize_phone_number(value)

    if not PHONE_PATTERN.match(normalized_value):
        raise ValidationError(
            _("Введите корректный номер телефона в международном формате.")
        )
