from __future__ import annotations

from typing import Any

from apps.course.models import Course
from apps.course.selectors import get_course_by_id
from apps.course.services.course.payloads import COURSE_MUTABLE_FIELDS
from apps.course.services.course.validation import validate_course_can_be_saved
from django.db import transaction


@transaction.atomic
def create_course(
    *,
    data: dict[str, Any],
) -> Course:
    """
    Создаёт курс.
    """

    course = Course()

    _apply_course_data(
        course=course,
        data=data,
    )

    validate_course_can_be_saved(course=course)

    course.full_clean()
    course.save()

    return course


@transaction.atomic
def update_course(
    *,
    course: Course,
    data: dict[str, Any],
) -> Course:
    """
    Обновляет курс.
    """

    _apply_course_data(
        course=course,
        data=data,
    )

    validate_course_can_be_saved(course=course)

    course.full_clean()
    course.save()

    return course


@transaction.atomic
def update_course_by_id(
    *,
    course_id: int,
    data: dict[str, Any],
) -> Course:
    """
    Обновляет курс по идентификатору.
    """

    course = get_course_by_id(course_id)

    return update_course(
        course=course,
        data=data,
    )


def _apply_course_data(
    *,
    course: Course,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к курсу.
    """

    for field_name in COURSE_MUTABLE_FIELDS:
        if field_name in data:
            setattr(course, field_name, data[field_name])
