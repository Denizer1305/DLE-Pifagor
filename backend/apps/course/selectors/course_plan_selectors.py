from __future__ import annotations

from apps.course.models import CoursePlan
from django.db.models import Q, QuerySet


def course_plan_base_queryset() -> QuerySet[CoursePlan]:
    """
    Возвращает базовый queryset КТП.
    """

    return CoursePlan.objects.select_related(
        "course",
        "course__owner_teacher",
        "course__organization",
        "course__subject",
        "course__academic_year",
        "course__period",
    )


def course_plan_list_queryset(
    *,
    search: str | None = None,
    course_id: int | None = None,
    status: str | None = None,
    semester_number: int | None = None,
    is_active: bool | None = None,
) -> QuerySet[CoursePlan]:
    """
    Возвращает список КТП.
    """

    queryset = course_plan_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(course__title__icontains=search)
            | Q(course__code__icontains=search)
            | Q(discipline_name__icontains=search)
            | Q(discipline_code__icontains=search)
            | Q(specialty_code__icontains=search)
            | Q(specialty_name__icontains=search)
            | Q(teacher_name_snapshot__icontains=search)
            | Q(organization_name_snapshot__icontains=search)
            | Q(academic_year_label__icontains=search)
        )

    if course_id:
        queryset = queryset.filter(course_id=course_id)

    if status:
        queryset = queryset.filter(status=status)

    if semester_number:
        queryset = queryset.filter(semester_number=semester_number)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset.order_by(
        "course__organization_id",
        "course__subject_id",
        "-updated_at",
    )


def course_plan_detail_queryset() -> QuerySet[CoursePlan]:
    """
    Возвращает queryset КТП с деталями.
    """

    return course_plan_base_queryset().prefetch_related(
        "imports",
    )


def get_course_plan_by_id(
    plan_id: int,
) -> CoursePlan:
    """
    Возвращает КТП по идентификатору.
    """

    return course_plan_detail_queryset().get(id=plan_id)


def get_course_plan_by_course_id(
    course_id: int,
) -> CoursePlan:
    """
    Возвращает КТП по курсу.
    """

    return course_plan_detail_queryset().get(course_id=course_id)
