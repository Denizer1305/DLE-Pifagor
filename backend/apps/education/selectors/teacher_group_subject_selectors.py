from __future__ import annotations

from apps.education.models import TeacherGroupSubject
from django.db.models import Q, QuerySet


def teacher_group_subject_base_queryset() -> QuerySet:
    """
    Базовый queryset назначений преподавателей на предметы групп.
    """

    return TeacherGroupSubject.objects.select_related(
        "teacher",
        "group_subject",
        "group_subject__group",
        "group_subject__group__organization",
        "group_subject__group__department",
        "group_subject__subject",
        "group_subject__academic_year",
        "group_subject__period",
    )


def teacher_group_subject_list_queryset(
    *,
    search: str = "",
    teacher_id: int | None = None,
    organization_id: int | None = None,
    department_id: int | None = None,
    group_id: int | None = None,
    subject_id: int | None = None,
    academic_year_id: int | None = None,
    period_id: int | None = None,
    role: str = "",
    is_primary: bool | None = None,
    is_active: bool | None = None,
) -> QuerySet:
    """
    Возвращает список назначений преподавателей с фильтрами.
    """

    queryset = teacher_group_subject_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(teacher__email__icontains=search)
            | Q(teacher__first_name__icontains=search)
            | Q(teacher__last_name__icontains=search)
            | Q(group_subject__group__name__icontains=search)
            | Q(group_subject__group__code__icontains=search)
            | Q(group_subject__subject__name__icontains=search)
            | Q(group_subject__subject__short_name__icontains=search)
            | Q(group_subject__subject__code__icontains=search)
        )

    if teacher_id:
        queryset = queryset.filter(teacher_id=teacher_id)

    if organization_id:
        queryset = queryset.filter(
            group_subject__group__organization_id=organization_id,
        )

    if department_id:
        queryset = queryset.filter(
            group_subject__group__department_id=department_id,
        )

    if group_id:
        queryset = queryset.filter(group_subject__group_id=group_id)

    if subject_id:
        queryset = queryset.filter(group_subject__subject_id=subject_id)

    if academic_year_id:
        queryset = queryset.filter(group_subject__academic_year_id=academic_year_id)

    if period_id:
        queryset = queryset.filter(group_subject__period_id=period_id)

    if role:
        queryset = queryset.filter(role=role)

    if is_primary is not None:
        queryset = queryset.filter(is_primary=is_primary)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset


def teacher_group_subject_detail_queryset() -> QuerySet:
    """
    Queryset для детальной карточки назначения преподавателя.
    """

    return teacher_group_subject_base_queryset()


def get_teacher_group_subject_by_id(
    teacher_group_subject_id: int,
) -> TeacherGroupSubject:
    """
    Возвращает назначение преподавателя по идентификатору.
    """

    return teacher_group_subject_detail_queryset().get(
        id=teacher_group_subject_id,
    )


def get_active_assignments_for_teacher(
    teacher_id: int,
    *,
    academic_year_id: int | None = None,
    period_id: int | None = None,
) -> QuerySet:
    """
    Возвращает активные назначения преподавателя.
    """

    queryset = teacher_group_subject_base_queryset().filter(
        teacher_id=teacher_id,
        is_active=True,
    )

    if academic_year_id:
        queryset = queryset.filter(group_subject__academic_year_id=academic_year_id)

    if period_id:
        queryset = queryset.filter(group_subject__period_id=period_id)

    return queryset
