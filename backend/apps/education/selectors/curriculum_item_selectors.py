from __future__ import annotations

from apps.education.models import CurriculumItem
from django.db.models import Q, QuerySet


def curriculum_item_base_queryset() -> QuerySet:
    """
    Базовый queryset элементов учебного плана.
    """

    return CurriculumItem.objects.select_related(
        "curriculum",
        "curriculum__organization",
        "curriculum__department",
        "curriculum__academic_year",
        "period",
        "subject",
    )


def curriculum_item_list_queryset(
    *,
    search: str = "",
    curriculum_id: int | None = None,
    organization_id: int | None = None,
    department_id: int | None = None,
    academic_year_id: int | None = None,
    period_id: int | None = None,
    subject_id: int | None = None,
    assessment_type: str = "",
    is_required: bool | None = None,
    is_active: bool | None = None,
) -> QuerySet:
    """
    Возвращает список элементов учебного плана с фильтрами.
    """

    queryset = curriculum_item_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(curriculum__name__icontains=search)
            | Q(curriculum__code__icontains=search)
            | Q(subject__name__icontains=search)
            | Q(subject__short_name__icontains=search)
            | Q(subject__code__icontains=search)
            | Q(period__name__icontains=search)
            | Q(period__code__icontains=search)
        )

    if curriculum_id:
        queryset = queryset.filter(curriculum_id=curriculum_id)

    if organization_id:
        queryset = queryset.filter(curriculum__organization_id=organization_id)

    if department_id:
        queryset = queryset.filter(curriculum__department_id=department_id)

    if academic_year_id:
        queryset = queryset.filter(curriculum__academic_year_id=academic_year_id)

    if period_id:
        queryset = queryset.filter(period_id=period_id)

    if subject_id:
        queryset = queryset.filter(subject_id=subject_id)

    if assessment_type:
        queryset = queryset.filter(assessment_type=assessment_type)

    if is_required is not None:
        queryset = queryset.filter(is_required=is_required)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset


def curriculum_item_detail_queryset() -> QuerySet:
    """
    Queryset для детальной карточки элемента учебного плана.
    """

    return curriculum_item_base_queryset().prefetch_related(
        "group_subjects",
    )


def get_curriculum_item_by_id(curriculum_item_id: int) -> CurriculumItem:
    """
    Возвращает элемент учебного плана по идентификатору.
    """

    return curriculum_item_detail_queryset().get(id=curriculum_item_id)


def get_active_items_for_curriculum(curriculum_id: int) -> QuerySet:
    """
    Возвращает активные элементы учебного плана.
    """

    return curriculum_item_base_queryset().filter(
        curriculum_id=curriculum_id,
        is_active=True,
    )
