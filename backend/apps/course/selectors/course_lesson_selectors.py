from __future__ import annotations

from apps.course.models import CourseLesson
from django.db.models import Q, QuerySet


def course_lesson_base_queryset() -> QuerySet[CourseLesson]:
    """
    Возвращает базовый queryset уроков курса.
    """

    return CourseLesson.objects.select_related(
        "course",
        "section",
        "course__owner_teacher",
        "course__organization",
        "course__subject",
    )


def course_lesson_list_queryset(
    *,
    search: str | None = None,
    course_id: int | None = None,
    section_id: int | None = None,
    lesson_type: str | None = None,
    is_required: bool | None = None,
    is_preview: bool | None = None,
    is_published: bool | None = None,
    is_active: bool | None = None,
) -> QuerySet[CourseLesson]:
    """
    Возвращает список уроков курса.
    """

    queryset = course_lesson_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(title__icontains=search)
            | Q(short_content__icontains=search)
            | Q(visual_aids__icontains=search)
            | Q(literature__icontains=search)
            | Q(independent_work__icontains=search)
            | Q(notes__icontains=search)
            | Q(course__title__icontains=search)
            | Q(course__code__icontains=search)
            | Q(section__title__icontains=search)
        )

    if course_id:
        queryset = queryset.filter(course_id=course_id)

    if section_id:
        queryset = queryset.filter(section_id=section_id)

    if lesson_type:
        queryset = queryset.filter(lesson_type=lesson_type)

    if is_required is not None:
        queryset = queryset.filter(is_required=is_required)

    if is_preview is not None:
        queryset = queryset.filter(is_preview=is_preview)

    if is_published is not None:
        queryset = queryset.filter(is_published=is_published)

    if is_active is not None:
        queryset = queryset.filter(is_active=is_active)

    return queryset.order_by(
        "course_id",
        "section__order",
        "order",
        "lesson_number",
    )


def course_lesson_detail_queryset() -> QuerySet[CourseLesson]:
    """
    Возвращает queryset урока с деталями.
    """

    return course_lesson_base_queryset().prefetch_related(
        "blocks",
        "material_links",
        "progresses",
    )


def get_course_lesson_by_id(
    lesson_id: int,
) -> CourseLesson:
    """
    Возвращает урок курса по идентификатору.
    """

    return course_lesson_detail_queryset().get(id=lesson_id)
