from __future__ import annotations

from apps.education.models import EducationPeriod
from django.db.models import Q, QuerySet


def education_period_base_queryset() -> QuerySet:
    """
    Базовый queryset учебных периодов.
    """

    return EducationPeriod.objects.select_related(
        "academic_year",
    )


def education_period_list_queryset(
    *,
    search: str = "",
    academic_year_id: int | None = None,
    period_type: str = "",
    is_active: bool | None = None,
    is_current: bool | None = None,
) -> QuerySet:
    """
    Возвращает список учебных периодов с фильтрами.
    """

    queryset = education_period_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(name__icontains=search)
            | Q(code__icontains=search)
            | Q(academic_year__name__icontains=search)
        )

    if academic_year_id:
        queryset = queryset.filter(academic_year_id=academic_year_id)

    if period_type:
        queryset = queryset.filter(period_type=period_type)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    if is_current is not None:
        queryset = queryset.filter(is_current=is_current)

    return queryset


def education_period_detail_queryset() -> QuerySet:
    """
    Queryset для детальной карточки учебного периода.
    """

    return education_period_base_queryset().prefetch_related(
        "curriculum_items",
        "group_subjects",
    )


def get_education_period_by_id(period_id: int) -> EducationPeriod:
    """
    Возвращает учебный период по идентификатору.
    """

    return education_period_detail_queryset().get(id=period_id)


def get_current_education_period(
    *,
    academic_year_id: int | None = None,
) -> EducationPeriod | None:
    """
    Возвращает текущий учебный период.
    """

    queryset = education_period_base_queryset().filter(is_current=True)

    if academic_year_id:
        queryset = queryset.filter(academic_year_id=academic_year_id)

    return queryset.first()


def get_active_periods_for_year(academic_year_id: int) -> QuerySet:
    """
    Возвращает активные периоды учебного года.
    """

    return education_period_base_queryset().filter(
        academic_year_id=academic_year_id,
        is_active=True,
    )
