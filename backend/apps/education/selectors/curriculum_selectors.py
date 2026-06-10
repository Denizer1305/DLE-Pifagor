from __future__ import annotations

from apps.education.models import Curriculum
from django.db.models import Q, QuerySet


def curriculum_base_queryset() -> QuerySet:
    """
    Базовый queryset учебных планов.
    """

    return Curriculum.objects.select_related(
        "organization",
        "department",
        "academic_year",
    )


def curriculum_list_queryset(
    *,
    search: str = "",
    organization_id: int | None = None,
    department_id: int | None = None,
    academic_year_id: int | None = None,
    status: str = "",
    is_active: bool | None = None,
) -> QuerySet:
    """
    Возвращает список учебных планов с фильтрами.
    """

    queryset = curriculum_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(name__icontains=search)
            | Q(code__icontains=search)
            | Q(organization__name__icontains=search)
            | Q(organization__short_name__icontains=search)
            | Q(department__name__icontains=search)
            | Q(department__short_name__icontains=search)
        )

    if organization_id:
        queryset = queryset.filter(organization_id=organization_id)

    if department_id:
        queryset = queryset.filter(department_id=department_id)

    if academic_year_id:
        queryset = queryset.filter(academic_year_id=academic_year_id)

    if status:
        queryset = queryset.filter(status=status)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset


def curriculum_detail_queryset() -> QuerySet:
    """
    Queryset для детальной карточки учебного плана.
    """

    return curriculum_base_queryset().prefetch_related(
        "items",
        "items__period",
        "items__subject",
    )


def get_curriculum_by_id(curriculum_id: int) -> Curriculum:
    """
    Возвращает учебный план по идентификатору.
    """

    return curriculum_detail_queryset().get(id=curriculum_id)


def get_active_curricula_for_organization(
    organization_id: int,
    *,
    academic_year_id: int | None = None,
) -> QuerySet:
    """
    Возвращает активные учебные планы организации.
    """

    queryset = curriculum_base_queryset().filter(
        organization_id=organization_id,
        is_active=True,
    )

    if academic_year_id:
        queryset = queryset.filter(academic_year_id=academic_year_id)

    return queryset
