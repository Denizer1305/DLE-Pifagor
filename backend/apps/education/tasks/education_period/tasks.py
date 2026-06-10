from __future__ import annotations

from datetime import date
from typing import Any

from apps.education.models import EducationPeriod
from apps.education.selectors import get_current_academic_year
from apps.education.services import (
    deactivate_education_period,
    set_current_education_period,
)
from django.utils import timezone


def refresh_current_education_period(
    *,
    reference_date: date | None = None,
    academic_year_id: int | None = None,
) -> dict[str, Any]:
    """
    Обновляет текущий учебный период по дате.

    Если academic_year_id не передан, используется текущий учебный год.
    """

    current_date = reference_date or timezone.localdate()
    resolved_academic_year_id = academic_year_id

    if resolved_academic_year_id is None:
        current_academic_year = get_current_academic_year()

        if current_academic_year is not None:
            resolved_academic_year_id = current_academic_year.id

    queryset = EducationPeriod.objects.filter(
        is_active=True,
        start_date__lte=current_date,
        end_date__gte=current_date,
    )

    if resolved_academic_year_id:
        queryset = queryset.filter(academic_year_id=resolved_academic_year_id)

    period = queryset.order_by("sequence", "start_date").first()

    if period is None:
        reset_queryset = EducationPeriod.objects.filter(is_current=True)

        if resolved_academic_year_id:
            reset_queryset = reset_queryset.filter(
                academic_year_id=resolved_academic_year_id,
            )

        updated_count = reset_queryset.update(is_current=False)

        return {
            "updated": updated_count,
            "current_period_id": None,
        }

    if not period.is_current:
        set_current_education_period(period=period)

    return {
        "updated": 1,
        "current_period_id": period.id,
    }


def deactivate_past_education_periods(
    *,
    reference_date: date | None = None,
) -> dict[str, int]:
    """
    Деактивирует прошедшие учебные периоды.
    """

    current_date = reference_date or timezone.localdate()

    periods = EducationPeriod.objects.filter(
        is_active=True,
        is_current=False,
        end_date__lt=current_date,
    )

    updated_count = 0

    for period in periods:
        deactivate_education_period(period=period)
        updated_count += 1

    return {
        "updated": updated_count,
    }
