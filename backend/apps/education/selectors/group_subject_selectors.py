from __future__ import annotations

from apps.education.models import GroupSubject
from django.db.models import Q, QuerySet


def group_subject_base_queryset() -> QuerySet:
    """
    Базовый queryset предметов учебных групп.
    """

    return GroupSubject.objects.select_related(
        "group",
        "group__organization",
        "group__department",
        "subject",
        "academic_year",
        "period",
        "curriculum_item",
        "curriculum_item__curriculum",
    )


def group_subject_list_queryset(
    *,
    search: str = "",
    organization_id: int | None = None,
    department_id: int | None = None,
    group_id: int | None = None,
    subject_id: int | None = None,
    academic_year_id: int | None = None,
    period_id: int | None = None,
    assessment_type: str = "",
    is_required: bool | None = None,
    is_active: bool | None = None,
) -> QuerySet:
    """
    Возвращает список предметов групп с фильтрами.
    """

    queryset = group_subject_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(group__name__icontains=search)
            | Q(group__code__icontains=search)
            | Q(subject__name__icontains=search)
            | Q(subject__short_name__icontains=search)
            | Q(subject__code__icontains=search)
            | Q(period__name__icontains=search)
            | Q(period__code__icontains=search)
        )

    if organization_id:
        queryset = queryset.filter(group__organization_id=organization_id)

    if department_id:
        queryset = queryset.filter(group__department_id=department_id)

    if group_id:
        queryset = queryset.filter(group_id=group_id)

    if subject_id:
        queryset = queryset.filter(subject_id=subject_id)

    if academic_year_id:
        queryset = queryset.filter(academic_year_id=academic_year_id)

    if period_id:
        queryset = queryset.filter(period_id=period_id)

    if assessment_type:
        queryset = queryset.filter(assessment_type=assessment_type)

    if is_required is not None:
        queryset = queryset.filter(is_required=is_required)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset


def group_subject_detail_queryset() -> QuerySet:
    """
    Queryset для детальной карточки предмета группы.
    """

    return group_subject_base_queryset().prefetch_related(
        "teacher_assignments",
        "teacher_assignments__teacher",
    )


def get_group_subject_by_id(group_subject_id: int) -> GroupSubject:
    """
    Возвращает предмет группы по идентификатору.
    """

    return group_subject_detail_queryset().get(id=group_subject_id)


def get_active_group_subjects_for_group(
    group_id: int,
    *,
    academic_year_id: int | None = None,
    period_id: int | None = None,
) -> QuerySet:
    """
    Возвращает активные предметы конкретной группы.
    """

    queryset = group_subject_base_queryset().filter(
        group_id=group_id,
        is_active=True,
    )

    if academic_year_id:
        queryset = queryset.filter(academic_year_id=academic_year_id)

    if period_id:
        queryset = queryset.filter(period_id=period_id)

    return queryset
