from __future__ import annotations

from datetime import date
from typing import Any

from apps.education.models import AcademicYear
from apps.education.services import deactivate_academic_year, set_current_academic_year
from django.utils import timezone


def refresh_current_academic_year(
    *,
    reference_date: date | None = None,
) -> dict[str, Any]:
    """
    Обновляет текущий учебный год по дате.

    Если на дату найден активный учебный год, он становится текущим.
    Если учебный год не найден, текущий флаг снимается со всех годов.
    """

    current_date = reference_date or timezone.localdate()

    academic_year = (
        AcademicYear.objects.filter(
            is_active=True,
            start_date__lte=current_date,
            end_date__gte=current_date,
        )
        .order_by("-start_date")
        .first()
    )

    if academic_year is None:
        updated_count = AcademicYear.objects.filter(
            is_current=True,
        ).update(is_current=False)

        return {
            "updated": updated_count,
            "current_academic_year_id": None,
        }

    if not academic_year.is_current:
        set_current_academic_year(academic_year=academic_year)

    return {
        "updated": 1,
        "current_academic_year_id": academic_year.id,
    }


def deactivate_past_academic_years(
    *,
    reference_date: date | None = None,
) -> dict[str, int]:
    """
    Деактивирует прошедшие учебные годы.

    Текущий учебный год не трогается.
    """

    current_date = reference_date or timezone.localdate()

    academic_years = AcademicYear.objects.filter(
        is_active=True,
        is_current=False,
        end_date__lt=current_date,
    )

    updated_count = 0

    for academic_year in academic_years:
        deactivate_academic_year(academic_year=academic_year)
        updated_count += 1

    return {
        "updated": updated_count,
    }
