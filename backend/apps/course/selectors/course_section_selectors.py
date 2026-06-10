from __future__ import annotations

from apps.course.models import CourseSection
from django.db.models import Q, QuerySet


def course_section_base_queryset() -> QuerySet[CourseSection]:
    """
    Возвращает базовый queryset разделов курса.
    """

    return CourseSection.objects.select_related(
        "course",
        "course__owner_teacher",
        "course__organization",
        "course__subject",
    )


def course_section_list_queryset(
    *,
    search: str | None = None,
    course_id: int | None = None,
    is_required: bool | None = None,
    is_published: bool | None = None,
    is_active: bool | None = None,
) -> QuerySet[CourseSection]:
    """
    Возвращает список разделов курса.
    """

    queryset = course_section_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
            | Q(course__title__icontains=search)
            | Q(course__code__icontains=search)
        )

    if course_id:
        queryset = queryset.filter(course_id=course_id)

    if is_required is not None:
        queryset = queryset.filter(is_required=is_required)

    if is_published is not None:
        queryset = queryset.filter(is_published=is_published)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset.order_by(
        "course_id",
        "order",
        "section_number",
        "title",
    )


def course_section_detail_queryset() -> QuerySet[CourseSection]:
    """
    Возвращает queryset раздела с деталями.
    """

    return course_section_base_queryset().prefetch_related(
        "lessons",
        "material_links",
    )


def get_course_section_by_id(
    section_id: int,
) -> CourseSection:
    """
    Возвращает раздел курса по идентификатору.
    """

    return course_section_detail_queryset().get(id=section_id)
