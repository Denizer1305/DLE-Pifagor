from __future__ import annotations

from typing import Any

from apps.education.models import AcademicYear
from apps.education.selectors import get_academic_year_by_id
from django.db import transaction

ACADEMIC_YEAR_MUTABLE_FIELDS = {
    "name",
    "start_date",
    "end_date",
    "description",
    "is_current",
    "is_active",
}


@transaction.atomic
def create_academic_year(*, data: dict[str, Any]) -> AcademicYear:
    """
    Создаёт учебный год.
    """

    academic_year = AcademicYear()

    _apply_academic_year_data(
        academic_year=academic_year,
        data=data,
    )

    if academic_year.is_current:
        _unset_other_current_academic_years()

    academic_year.full_clean()
    academic_year.save()

    return academic_year


@transaction.atomic
def update_academic_year(
    *,
    academic_year: AcademicYear,
    data: dict[str, Any],
) -> AcademicYear:
    """
    Обновляет учебный год.
    """

    _apply_academic_year_data(
        academic_year=academic_year,
        data=data,
    )

    if academic_year.is_current:
        _unset_other_current_academic_years(exclude_id=academic_year.id)

    academic_year.full_clean()
    academic_year.save()

    return academic_year


@transaction.atomic
def update_academic_year_by_id(
    *,
    academic_year_id: int,
    data: dict[str, Any],
) -> AcademicYear:
    """
    Обновляет учебный год по идентификатору.
    """

    academic_year = get_academic_year_by_id(academic_year_id)

    return update_academic_year(
        academic_year=academic_year,
        data=data,
    )


@transaction.atomic
def set_current_academic_year(
    *,
    academic_year: AcademicYear,
) -> AcademicYear:
    """
    Делает учебный год текущим.
    """

    _unset_other_current_academic_years(exclude_id=academic_year.id)

    academic_year.is_current = True
    academic_year.is_active = True
    academic_year.full_clean()
    academic_year.save(
        update_fields=[
            "is_current",
            "is_active",
            "updated_at",
        ],
    )

    return academic_year


@transaction.atomic
def set_current_academic_year_by_id(
    *,
    academic_year_id: int,
) -> AcademicYear:
    """
    Делает учебный год текущим по идентификатору.
    """

    academic_year = get_academic_year_by_id(academic_year_id)

    return set_current_academic_year(academic_year=academic_year)


@transaction.atomic
def deactivate_academic_year(
    *,
    academic_year: AcademicYear,
) -> AcademicYear:
    """
    Деактивирует учебный год.
    """

    academic_year.is_active = False

    if academic_year.is_current:
        academic_year.is_current = False

    academic_year.full_clean()
    academic_year.save(
        update_fields=[
            "is_active",
            "is_current",
            "updated_at",
        ],
    )

    return academic_year


@transaction.atomic
def deactivate_academic_year_by_id(
    *,
    academic_year_id: int,
) -> AcademicYear:
    """
    Деактивирует учебный год по идентификатору.
    """

    academic_year = get_academic_year_by_id(academic_year_id)

    return deactivate_academic_year(academic_year=academic_year)


@transaction.atomic
def restore_academic_year(
    *,
    academic_year: AcademicYear,
) -> AcademicYear:
    """
    Восстанавливает учебный год.
    """

    academic_year.is_active = True
    academic_year.full_clean()
    academic_year.save(
        update_fields=[
            "is_active",
            "updated_at",
        ],
    )

    return academic_year


@transaction.atomic
def restore_academic_year_by_id(
    *,
    academic_year_id: int,
) -> AcademicYear:
    """
    Восстанавливает учебный год по идентификатору.
    """

    academic_year = get_academic_year_by_id(academic_year_id)

    return restore_academic_year(academic_year=academic_year)


def _apply_academic_year_data(
    *,
    academic_year: AcademicYear,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к учебному году.
    """

    for field_name in ACADEMIC_YEAR_MUTABLE_FIELDS:
        if field_name in data:
            setattr(academic_year, field_name, data[field_name])


def _unset_other_current_academic_years(
    *,
    exclude_id: int | None = None,
) -> None:
    """
    Снимает флаг текущего учебного года со всех остальных годов.
    """

    queryset = AcademicYear.objects.filter(is_current=True)

    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)

    queryset.update(is_current=False)
