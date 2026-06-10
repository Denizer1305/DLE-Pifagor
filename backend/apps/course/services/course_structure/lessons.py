from __future__ import annotations

from typing import Any

from apps.course.models import CourseLesson
from apps.course.selectors import get_course_lesson_by_id
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _

COURSE_LESSON_MUTABLE_FIELDS = {
    "course",
    "course_id",
    "section",
    "section_id",
    "lesson_number",
    "lesson_type",
    "title",
    "short_content",
    "planned_hours",
    "theory_hours",
    "practice_hours",
    "lab_hours",
    "self_study_hours",
    "visual_aids",
    "literature",
    "independent_work",
    "notes",
    "order",
    "available_from",
    "is_required",
    "is_preview",
    "is_published",
    "is_active",
}


@transaction.atomic
def create_course_lesson(
    *,
    data: dict[str, Any],
) -> CourseLesson:
    """
    Создаёт урок курса.
    """

    lesson = CourseLesson()

    _apply_course_lesson_data(
        lesson=lesson,
        data=data,
    )

    validate_course_lesson_can_be_saved(lesson=lesson)

    lesson.full_clean()
    lesson.save()

    return lesson


@transaction.atomic
def update_course_lesson(
    *,
    lesson: CourseLesson,
    data: dict[str, Any],
) -> CourseLesson:
    """
    Обновляет урок курса.
    """

    _apply_course_lesson_data(
        lesson=lesson,
        data=data,
    )

    validate_course_lesson_can_be_saved(lesson=lesson)

    lesson.full_clean()
    lesson.save()

    return lesson


@transaction.atomic
def update_course_lesson_by_id(
    *,
    lesson_id: int,
    data: dict[str, Any],
) -> CourseLesson:
    """
    Обновляет урок курса по идентификатору.
    """

    lesson = get_course_lesson_by_id(lesson_id)

    return update_course_lesson(
        lesson=lesson,
        data=data,
    )


@transaction.atomic
def publish_course_lesson(
    *,
    lesson: CourseLesson,
) -> CourseLesson:
    """
    Публикует урок курса.
    """

    lesson.is_published = True
    lesson.is_active = True
    lesson.full_clean()
    lesson.save(
        update_fields=[
            "is_published",
            "is_active",
            "updated_at",
        ],
    )

    return lesson


@transaction.atomic
def archive_course_lesson(
    *,
    lesson: CourseLesson,
) -> CourseLesson:
    """
    Архивирует урок курса.
    """

    lesson.is_published = False
    lesson.is_active = False
    lesson.full_clean()
    lesson.save(
        update_fields=[
            "is_published",
            "is_active",
            "updated_at",
        ],
    )

    return lesson


def validate_course_lesson_can_be_saved(
    *,
    lesson: CourseLesson,
) -> None:
    """
    Проверяет, что урок курса можно сохранить.
    """

    if lesson.section_id and lesson.course_id:
        if lesson.section.course_id != lesson.course_id:
            raise ValidationError(
                {"section": _("Раздел должен относиться к тому же курсу.")}
            )


def _apply_course_lesson_data(
    *,
    lesson: CourseLesson,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к уроку курса.
    """

    for field_name in COURSE_LESSON_MUTABLE_FIELDS:
        if field_name in data:
            setattr(lesson, field_name, data[field_name])
