from __future__ import annotations

from collections.abc import Iterable

from apps.course.models import CourseEnrollment
from apps.course.services import (
    ensure_course_progress,
    ensure_lesson_progresses_for_enrollment,
    recalculate_course_progress,
)
from django.db import transaction


@transaction.atomic
def ensure_progress_for_active_enrollments(
    *,
    enrollment_ids: Iterable[int] | None = None,
) -> dict[str, int]:
    """
    Создаёт недостающий прогресс для активных записей на курс.
    """

    queryset = CourseEnrollment.objects.exclude(
        status__in=[
            CourseEnrollment.StatusChoices.CANCELLED,
            CourseEnrollment.StatusChoices.ARCHIVED,
        ],
    )

    if enrollment_ids is not None:
        queryset = queryset.filter(id__in=enrollment_ids)

    checked_count = 0
    course_progress_count = 0
    lesson_progress_created_count = 0

    for enrollment in queryset.select_related("course").iterator():
        ensure_course_progress(enrollment=enrollment)
        course_progress_count += 1

        result = ensure_lesson_progresses_for_enrollment(
            enrollment=enrollment,
        )
        lesson_progress_created_count += result["created"]

        checked_count += 1

    return {
        "checked": checked_count,
        "course_progress": course_progress_count,
        "lesson_progress_created": lesson_progress_created_count,
    }


@transaction.atomic
def recalculate_progress_for_active_enrollments(
    *,
    enrollment_ids: Iterable[int] | None = None,
) -> dict[str, int]:
    """
    Пересчитывает прогресс активных записей на курс.
    """

    queryset = CourseEnrollment.objects.exclude(
        status__in=[
            CourseEnrollment.StatusChoices.CANCELLED,
            CourseEnrollment.StatusChoices.ARCHIVED,
        ],
    )

    if enrollment_ids is not None:
        queryset = queryset.filter(id__in=enrollment_ids)

    recalculated_count = 0

    for enrollment in queryset.select_related("course").iterator():
        recalculate_course_progress(enrollment=enrollment)
        recalculated_count += 1

    return {
        "recalculated": recalculated_count,
    }


def collect_course_progress_stats() -> dict[str, int]:
    """
    Собирает статистику прогресса по курсам.
    """

    return {
        "enrollments_total": CourseEnrollment.objects.count(),
        "enrollments_not_started": CourseEnrollment.objects.filter(
            status=CourseEnrollment.StatusChoices.NOT_STARTED,
        ).count(),
        "enrollments_in_progress": CourseEnrollment.objects.filter(
            status=CourseEnrollment.StatusChoices.IN_PROGRESS,
        ).count(),
        "enrollments_completed": CourseEnrollment.objects.filter(
            status=CourseEnrollment.StatusChoices.COMPLETED,
        ).count(),
        "enrollments_cancelled": CourseEnrollment.objects.filter(
            status=CourseEnrollment.StatusChoices.CANCELLED,
        ).count(),
        "enrollments_archived": CourseEnrollment.objects.filter(
            status=CourseEnrollment.StatusChoices.ARCHIVED,
        ).count(),
    }
