from __future__ import annotations

from apps.course.models import (
    CourseLesson,
    CourseLessonBlock,
    CourseMaterialLink,
    CourseSection,
)
from django.db import transaction
from django.db.models import Max, QuerySet


@transaction.atomic
def reorder_course_sections(
    *,
    course_id: int,
    ordered_section_ids: list[int],
) -> None:
    """
    Переупорядочивает разделы курса.
    """

    queryset = CourseSection.objects.filter(course_id=course_id)

    _reorder_queryset_by_ids(
        queryset=queryset,
        ordered_ids=ordered_section_ids,
    )


@transaction.atomic
def reorder_course_lessons(
    *,
    course_id: int,
    ordered_lesson_ids: list[int],
    section_id: int | None = None,
) -> None:
    """
    Переупорядочивает уроки курса.
    """

    queryset = CourseLesson.objects.filter(course_id=course_id)

    if section_id is not None:
        queryset = queryset.filter(section_id=section_id)

    _reorder_queryset_by_ids(
        queryset=queryset,
        ordered_ids=ordered_lesson_ids,
    )


@transaction.atomic
def reorder_lesson_blocks(
    *,
    lesson_id: int,
    ordered_block_ids: list[int],
) -> None:
    """
    Переупорядочивает блоки урока.
    """

    queryset = CourseLessonBlock.objects.filter(lesson_id=lesson_id)

    _reorder_queryset_by_ids(
        queryset=queryset,
        ordered_ids=ordered_block_ids,
    )


@transaction.atomic
def reorder_course_material_links(
    *,
    course_id: int,
    ordered_link_ids: list[int],
) -> None:
    """
    Переупорядочивает материалы курса.
    """

    queryset = CourseMaterialLink.objects.filter(course_id=course_id)

    _reorder_queryset_by_ids(
        queryset=queryset,
        ordered_ids=ordered_link_ids,
    )


def _reorder_queryset_by_ids(
    *,
    queryset: QuerySet,
    ordered_ids: list[int],
) -> None:
    """
    Безопасно переставляет order без нарушения уникальных ограничений.

    Прямая перестановка 1 -> 2 и 2 -> 1 ломается на UNIQUE constraint.
    Поэтому сначала переносим элементы во временный диапазон,
    затем выставляем финальные значения.
    """

    if not ordered_ids:
        return

    existing_ids = set(
        queryset.filter(id__in=ordered_ids).values_list(
            "id",
            flat=True,
        )
    )

    ordered_existing_ids = [
        object_id for object_id in ordered_ids if object_id in existing_ids
    ]

    if not ordered_existing_ids:
        return

    max_order = queryset.aggregate(value=Max("order"))["value"] or 0
    temp_offset = max_order + len(ordered_existing_ids) + 1000

    for index, object_id in enumerate(ordered_existing_ids, start=1):
        queryset.filter(id=object_id).update(order=temp_offset + index)

    for index, object_id in enumerate(ordered_existing_ids, start=1):
        queryset.filter(id=object_id).update(order=index)
