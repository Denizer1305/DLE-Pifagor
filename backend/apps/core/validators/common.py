from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_required_text(value: str | None, *, field_name: str = "Значение") -> None:
    """
    Проверяет, что текстовое значение заполнено.
    """

    if value is None or not str(value).strip():
        raise ValidationError(
            _("%(field_name)s обязательно для заполнения.")
            % {
                "field_name": field_name,
            }
        )


def validate_max_length(
    value: str | None,
    *,
    max_length: int,
    field_name: str = "Значение",
) -> None:
    """
    Проверяет максимальную длину текстового значения.
    """

    if value is None:
        return

    if len(str(value)) > max_length:
        raise ValidationError(
            _("%(field_name)s не должно быть длиннее %(max_length)s символов.")
            % {
                "field_name": field_name,
                "max_length": max_length,
            }
        )