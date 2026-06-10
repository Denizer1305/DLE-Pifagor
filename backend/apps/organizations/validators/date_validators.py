from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def validate_future_datetime(
    *,
    value,
    field_name: str,
    message: str,
) -> None:
    """
    Проверяет, что дата и время находятся в будущем.

    Args:
        value:
            Дата и время.
        field_name:
            Имя поля для ValidationError.
        message:
            Сообщение об ошибке.

    Raises:
        ValidationError: Если дата не в будущем.
    """

    if value is None:
        return

    if value <= timezone.now():
        raise ValidationError(
            {
                field_name: _(message),
            }
        )


def validate_date_range(
    *,
    starts_at,
    ends_at,
    field_name: str = "ends_at",
    message: str = "Дата окончания не может быть раньше даты начала.",
) -> None:
    """
    Проверяет диапазон дат.

    Args:
        starts_at:
            Дата начала.
        ends_at:
            Дата окончания.
        field_name:
            Имя поля для ValidationError.
        message:
            Сообщение об ошибке.

    Raises:
        ValidationError: Если дата окончания раньше даты начала.
    """

    if starts_at and ends_at and ends_at < starts_at:
        raise ValidationError(
            {
                field_name: _(message),
            }
        )


def validate_year_order(
    *,
    start_year: int | None,
    end_year: int | None,
    field_name: str = "graduation_year",
    message: str = "Год окончания не может быть раньше года начала.",
) -> None:
    """
    Проверяет порядок годов.

    Args:
        start_year:
            Начальный год.
        end_year:
            Конечный год.
        field_name:
            Имя поля для ValidationError.
        message:
            Сообщение об ошибке.

    Raises:
        ValidationError: Если конечный год раньше начального.
    """

    if start_year and end_year and end_year < start_year:
        raise ValidationError(
            {
                field_name: _(message),
            }
        )
