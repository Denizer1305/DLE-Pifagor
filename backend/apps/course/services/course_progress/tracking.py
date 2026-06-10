from __future__ import annotations

from apps.course.models import CourseEnrollment, CourseLesson
from apps.course.services.course_access import start_course_enrollment
from apps.course.services.course_progress.ensure import (
    _model_has_field,
    _save_model_fields,
    ensure_course_progress,
    ensure_lesson_progress,
)
from apps.course.services.course_progress.lessons import (
    complete_lesson_progress,
    start_lesson_progress,
)
from apps.course.services.course_progress.recalculation import (
    recalculate_course_progress,
)
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def track_lesson_opened(
    *,
    enrollment: CourseEnrollment,
    lesson: CourseLesson,
) -> dict:
    """
    Фиксирует открытие урока обучающимся.
    """

    lesson_progress = ensure_lesson_progress(
        enrollment=enrollment,
        lesson=lesson,
    )
    lesson_progress = start_lesson_progress(
        lesson_progress=lesson_progress,
    )

    start_course_enrollment(enrollment=enrollment)

    course_progress = _touch_course_progress(
        enrollment=enrollment,
        lesson=lesson,
    )

    return {
        "enrollment": enrollment,
        "course_progress": course_progress,
        "lesson_progress": lesson_progress,
    }


@transaction.atomic
def track_lesson_completed(
    *,
    enrollment: CourseEnrollment,
    lesson: CourseLesson,
) -> dict:
    """
    Фиксирует завершение урока обучающимся.
    """

    lesson_progress = ensure_lesson_progress(
        enrollment=enrollment,
        lesson=lesson,
    )
    lesson_progress = complete_lesson_progress(
        lesson_progress=lesson_progress,
    )

    course_progress = recalculate_course_progress(enrollment=enrollment)

    return {
        "enrollment": enrollment,
        "course_progress": course_progress,
        "lesson_progress": lesson_progress,
    }


@transaction.atomic
def touch_course_activity(
    *,
    enrollment: CourseEnrollment,
    lesson: CourseLesson | None = None,
):
    """
    Обновляет последнюю активность по курсу.
    """

    return _touch_course_progress(
        enrollment=enrollment,
        lesson=lesson,
    )


def _touch_course_progress(
    *,
    enrollment: CourseEnrollment,
    lesson: CourseLesson | None = None,
):
    """
    Обновляет дату последней активности прогресса курса.
    """

    course_progress = ensure_course_progress(enrollment=enrollment)

    now = timezone.now()

    if _model_has_field(type(course_progress), "last_activity_at"):
        course_progress.last_activity_at = now

    if lesson is not None and _model_has_field(type(course_progress), "last_lesson"):
        course_progress.last_lesson = lesson

    _save_model_fields(
        course_progress,
        [
            "last_activity_at",
            "last_lesson",
            "updated_at",
        ],
    )

    if _model_has_field(CourseEnrollment, "last_activity_at"):
        enrollment.last_activity_at = now
        _save_model_fields(
            enrollment,
            [
                "last_activity_at",
                "updated_at",
            ],
        )

    return course_progress
