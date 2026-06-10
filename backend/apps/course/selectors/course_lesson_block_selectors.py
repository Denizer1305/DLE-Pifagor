from __future__ import annotations

from apps.course.models import CourseLessonBlock
from django.db.models import Q, QuerySet


def course_lesson_block_base_queryset() -> QuerySet[CourseLessonBlock]:
    """
    Возвращает базовый queryset блоков уроков.
    """

    return CourseLessonBlock.objects.select_related(
        "lesson",
        "lesson__course",
        "lesson__section",
        "material",
    )


def course_lesson_block_list_queryset(
    *,
    search: str | None = None,
    lesson_id: int | None = None,
    block_type: str | None = None,
    material_id: int | None = None,
    is_visible: bool | None = None,
) -> QuerySet[CourseLessonBlock]:
    """
    Возвращает список блоков урока.
    """

    queryset = course_lesson_block_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(title__icontains=search)
            | Q(content__icontains=search)
            | Q(external_url__icontains=search)
            | Q(lesson__title__icontains=search)
            | Q(material__title__icontains=search)
            | Q(material__slug__icontains=search)
        )

    if lesson_id:
        queryset = queryset.filter(lesson_id=lesson_id)

    if block_type:
        queryset = queryset.filter(block_type=block_type)

    if material_id:
        queryset = queryset.filter(material_id=material_id)

    if is_visible is not None:
        queryset = queryset.filter(is_visible=is_visible)

    return queryset.order_by(
        "lesson_id",
        "order",
        "id",
    )


def course_lesson_block_detail_queryset() -> QuerySet[CourseLessonBlock]:
    """
    Возвращает queryset блока урока с деталями.
    """

    return course_lesson_block_base_queryset()


def get_course_lesson_block_by_id(
    block_id: int,
) -> CourseLessonBlock:
    """
    Возвращает блок урока по идентификатору.
    """

    return course_lesson_block_detail_queryset().get(id=block_id)
