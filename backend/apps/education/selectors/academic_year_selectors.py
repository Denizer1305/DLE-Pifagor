from __future__ import annotations

from apps.education.models import AcademicYear
from django.db.models import Q, QuerySet


def academic_year_base_queryset() -> QuerySet:
    """
    Базовый queryset учебных годов.
    """

    return AcademicYear.objects.all()


def academic_year_list_queryset(
    *,
    search: str = "",
    is_active: bool | None = None,
    is_current: bool | None = None,
) -> QuerySet:
    """
    Возвращает список учебных годов с базовыми фильтрами.
    """

    queryset = academic_year_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(name__icontains=search) | Q(description__icontains=search)
        )

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    if is_current is not None:
        queryset = queryset.filter(is_current=is_current)

    return queryset


def academic_year_detail_queryset() -> QuerySet:
    """
    Queryset для детальной карточки учебного года.
    """

    return academic_year_base_queryset().prefetch_related(
        "periods",
        "curricula",
    )


def get_academic_year_by_id(academic_year_id: int) -> AcademicYear:
    """
    Возвращает учебный год по идентификатору.
    """

    return academic_year_detail_queryset().get(id=academic_year_id)


def get_current_academic_year() -> AcademicYear | None:
    """
    Возвращает текущий учебный год, если он настроен.
    """

    return academic_year_base_queryset().filter(is_current=True).first()


def get_active_academic_years() -> QuerySet:
    """
    Возвращает активные учебные годы.
    """

    return academic_year_base_queryset().filter(is_active=True)
