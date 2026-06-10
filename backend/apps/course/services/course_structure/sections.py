from __future__ import annotations

from typing import Any

from apps.course.models import CourseSection
from apps.course.selectors import get_course_section_by_id
from django.db import transaction

COURSE_SECTION_MUTABLE_FIELDS = {
    "course",
    "course_id",
    "title",
    "description",
    "section_number",
    "order",
    "planned_hours",
    "is_required",
    "is_published",
    "is_active",
}


@transaction.atomic
def create_course_section(
    *,
    data: dict[str, Any],
) -> CourseSection:
    """
    Создаёт раздел курса.
    """

    section = CourseSection()

    _apply_course_section_data(
        section=section,
        data=data,
    )

    section.full_clean()
    section.save()

    return section


@transaction.atomic
def update_course_section(
    *,
    section: CourseSection,
    data: dict[str, Any],
) -> CourseSection:
    """
    Обновляет раздел курса.
    """

    _apply_course_section_data(
        section=section,
        data=data,
    )

    section.full_clean()
    section.save()

    return section


@transaction.atomic
def update_course_section_by_id(
    *,
    section_id: int,
    data: dict[str, Any],
) -> CourseSection:
    """
    Обновляет раздел курса по идентификатору.
    """

    section = get_course_section_by_id(section_id)

    return update_course_section(
        section=section,
        data=data,
    )


@transaction.atomic
def publish_course_section(
    *,
    section: CourseSection,
) -> CourseSection:
    """
    Публикует раздел курса.
    """

    section.is_published = True
    section.is_active = True
    section.full_clean()
    section.save(
        update_fields=[
            "is_published",
            "is_active",
            "updated_at",
        ],
    )

    return section


@transaction.atomic
def archive_course_section(
    *,
    section: CourseSection,
) -> CourseSection:
    """
    Архивирует раздел курса.
    """

    section.is_active = False
    section.is_published = False
    section.full_clean()
    section.save(
        update_fields=[
            "is_active",
            "is_published",
            "updated_at",
        ],
    )

    return section


def _apply_course_section_data(
    *,
    section: CourseSection,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к разделу курса.
    """

    for field_name in COURSE_SECTION_MUTABLE_FIELDS:
        if field_name in data:
            setattr(section, field_name, data[field_name])
