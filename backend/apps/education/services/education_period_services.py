from __future__ import annotations

from typing import Any

from apps.education.models import EducationPeriod
from apps.education.selectors import get_education_period_by_id
from django.db import transaction

EDUCATION_PERIOD_MUTABLE_FIELDS = {
    "academic_year",
    "academic_year_id",
    "name",
    "code",
    "period_type",
    "sequence",
    "start_date",
    "end_date",
    "description",
    "is_current",
    "is_active",
}


@transaction.atomic
def create_education_period(*, data: dict[str, Any]) -> EducationPeriod:
    """
    Создаёт учебный период.
    """

    period = EducationPeriod()

    _apply_education_period_data(
        period=period,
        data=data,
    )

    if period.is_current:
        _unset_other_current_periods(
            academic_year_id=period.academic_year_id,
        )

    period.full_clean()
    period.save()

    return period


@transaction.atomic
def update_education_period(
    *,
    period: EducationPeriod,
    data: dict[str, Any],
) -> EducationPeriod:
    """
    Обновляет учебный период.
    """

    _apply_education_period_data(
        period=period,
        data=data,
    )

    if period.is_current:
        _unset_other_current_periods(
            academic_year_id=period.academic_year_id,
            exclude_id=period.id,
        )

    period.full_clean()
    period.save()

    return period


@transaction.atomic
def update_education_period_by_id(
    *,
    period_id: int,
    data: dict[str, Any],
) -> EducationPeriod:
    """
    Обновляет учебный период по идентификатору.
    """

    period = get_education_period_by_id(period_id)

    return update_education_period(
        period=period,
        data=data,
    )


@transaction.atomic
def set_current_education_period(
    *,
    period: EducationPeriod,
) -> EducationPeriod:
    """
    Делает учебный период текущим внутри учебного года.
    """

    _unset_other_current_periods(
        academic_year_id=period.academic_year_id,
        exclude_id=period.id,
    )

    period.is_current = True
    period.is_active = True
    period.full_clean()
    period.save(
        update_fields=[
            "is_current",
            "is_active",
            "updated_at",
        ],
    )

    return period


@transaction.atomic
def set_current_education_period_by_id(
    *,
    period_id: int,
) -> EducationPeriod:
    """
    Делает учебный период текущим по идентификатору.
    """

    period = get_education_period_by_id(period_id)

    return set_current_education_period(period=period)


@transaction.atomic
def deactivate_education_period(
    *,
    period: EducationPeriod,
) -> EducationPeriod:
    """
    Деактивирует учебный период.
    """

    period.is_active = False

    if period.is_current:
        period.is_current = False

    period.full_clean()
    period.save(
        update_fields=[
            "is_active",
            "is_current",
            "updated_at",
        ],
    )

    return period


@transaction.atomic
def deactivate_education_period_by_id(
    *,
    period_id: int,
) -> EducationPeriod:
    """
    Деактивирует учебный период по идентификатору.
    """

    period = get_education_period_by_id(period_id)

    return deactivate_education_period(period=period)


@transaction.atomic
def restore_education_period(
    *,
    period: EducationPeriod,
) -> EducationPeriod:
    """
    Восстанавливает учебный период.
    """

    period.is_active = True
    period.full_clean()
    period.save(
        update_fields=[
            "is_active",
            "updated_at",
        ],
    )

    return period


@transaction.atomic
def restore_education_period_by_id(
    *,
    period_id: int,
) -> EducationPeriod:
    """
    Восстанавливает учебный период по идентификатору.
    """

    period = get_education_period_by_id(period_id)

    return restore_education_period(period=period)


def _apply_education_period_data(
    *,
    period: EducationPeriod,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к учебному периоду.
    """

    for field_name in EDUCATION_PERIOD_MUTABLE_FIELDS:
        if field_name in data:
            setattr(period, field_name, data[field_name])


def _unset_other_current_periods(
    *,
    academic_year_id: int,
    exclude_id: int | None = None,
) -> None:
    """
    Снимает флаг текущего периода у остальных периодов учебного года.
    """

    queryset = EducationPeriod.objects.filter(
        academic_year_id=academic_year_id,
        is_current=True,
    )

    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)

    queryset.update(is_current=False)
