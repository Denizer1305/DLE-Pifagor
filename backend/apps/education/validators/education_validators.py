from __future__ import annotations

import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

ACADEMIC_YEAR_PATTERN = re.compile(r"^\d{4}/\d{4}$")
CODE_PATTERN = re.compile(r"^[A-Za-zА-Яа-я0-9\-_]+$")


def validate_academic_year_name(value: str) -> None:
    """
    Проверяет название учебного года.

    Ожидаемый формат: 2025/2026.
    """

    if not value:
        raise ValidationError(_("Название учебного года обязательно."))

    normalized_value = value.strip()

    if not ACADEMIC_YEAR_PATTERN.fullmatch(normalized_value):
        raise ValidationError(_("Учебный год должен быть в формате ГГГГ/ГГГГ."))

    start_year, end_year = normalized_value.split("/")

    if int(end_year) != int(start_year) + 1:
        raise ValidationError(
            _("Учебный год должен состоять из двух последовательных лет.")
        )


def validate_code_value(value: str) -> None:
    """
    Проверяет технический код академической сущности.
    """

    if not value:
        raise ValidationError(_("Код обязателен."))

    normalized_value = value.strip()

    if not CODE_PATTERN.fullmatch(normalized_value):
        raise ValidationError(
            _("Код может содержать только буквы, цифры, дефис и подчёркивание.")
        )


def validate_period_code(value: str) -> None:
    """
    Проверяет код учебного периода.
    """

    validate_code_value(value)


def validate_curriculum_code(value: str) -> None:
    """
    Проверяет код учебного плана.
    """

    validate_code_value(value)
