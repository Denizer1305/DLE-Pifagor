from __future__ import annotations

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_positive_integer(value: int) -> None:
    """
    Проверяет, что число является положительным.
    """

    if value <= 0:
        raise ValidationError(_("Значение должно быть положительным числом."))


def validate_non_negative_number(value: int | float | Decimal) -> None:
    """
    Проверяет, что число не является отрицательным.
    """

    if value < 0:
        raise ValidationError(_("Значение не может быть отрицательным."))


def validate_positive_number(value: int | float | Decimal) -> None:
    """
    Проверяет, что число больше нуля.
    """

    if value <= 0:
        raise ValidationError(_("Значение должно быть больше нуля."))


def validate_number_not_greater_than(
    value: int | float | Decimal,
    *,
    max_value: int | float | Decimal,
    field_name: str = "Значение",
) -> None:
    """
    Проверяет, что число не больше заданного максимума.
    """

    if value > max_value:
        raise ValidationError(
            _("%(field_name)s не может быть больше %(max_value)s.")
            % {
                "field_name": field_name,
                "max_value": max_value,
            }
        )