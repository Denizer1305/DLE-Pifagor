from __future__ import annotations

from datetime import date

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def validate_birth_date_not_future(value: date) -> None:
    """
    Проверяет, что дата рождения не находится в будущем.
    """

    if value and value > date.today():
        raise ValidationError(_("Дата рождения не может быть в будущем."))


def validate_date_not_past(value: date | None) -> None:
    """
    Проверяет, что дата не находится в прошлом.
    """

    if value is None:
        return

    if value < timezone.localdate():
        raise ValidationError(_("Дата не может быть в прошлом."))


def validate_datetime_not_past(value) -> None:
    """
    Проверяет, что дата и время не находятся в прошлом.
    """

    if value is None:
        return

    if value < timezone.now():
        raise ValidationError(_("Дата и время не могут быть в прошлом."))