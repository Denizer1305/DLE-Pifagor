from __future__ import annotations

from apps.course.models import CourseEnrollment, CourseProgress, LessonProgress
from apps.course.selectors import get_course_enrollment_by_id
from apps.course.services.course_progress.ensure import (
    _get_lesson_status_value,
    _model_has_field,
    _save_model_fields,
    ensure_course_progress,
    ensure_lesson_progresses_for_enrollment,
)
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def recalculate_course_progress(
    *,
    enrollment: CourseEnrollment,
) -> CourseProgress:
    """
    Пересчитывает общий прогресс курса по прогрессу уроков.
    """

    ensure_lesson_progresses_for_enrollment(enrollment=enrollment)

    course_progress = ensure_course_progress(enrollment=enrollment)

    lessons_queryset = enrollment.course.lessons.filter(is_active=True)

    if _model_has_field(lessons_queryset.model, "is_published"):
        lessons_queryset = lessons_queryset.filter(is_published=True)

    total_lessons_count = lessons_queryset.count()

    completed_status = _get_lesson_status_value("COMPLETED", "completed")

    completed_lessons_count = LessonProgress.objects.filter(
        enrollment=enrollment,
        lesson__in=lessons_queryset,
        status=completed_status,
    ).count()

    progress_percent = _calculate_progress_percent(
        completed_lessons_count=completed_lessons_count,
        total_lessons_count=total_lessons_count,
    )

    if _model_has_field(CourseProgress, "total_lessons_count"):
        course_progress.total_lessons_count = total_lessons_count

    if _model_has_field(CourseProgress, "completed_lessons_count"):
        course_progress.completed_lessons_count = completed_lessons_count

    if _model_has_field(CourseProgress, "progress_percent"):
        course_progress.progress_percent = progress_percent

    last_lesson_progress = (
        LessonProgress.objects.filter(enrollment=enrollment)
        .select_related("lesson")
        .order_by(*_get_lesson_progress_activity_ordering())
        .first()
    )

    if (
        _model_has_field(CourseProgress, "last_lesson")
        and last_lesson_progress is not None
    ):
        course_progress.last_lesson = last_lesson_progress.lesson

    if _model_has_field(CourseProgress, "last_activity_at"):
        course_progress.last_activity_at = timezone.now()

    _save_model_fields(
        course_progress,
        [
            "total_lessons_count",
            "completed_lessons_count",
            "progress_percent",
            "last_lesson",
            "last_activity_at",
            "updated_at",
        ],
    )

    _sync_enrollment_progress(
        enrollment=enrollment,
        progress_percent=progress_percent,
    )

    return course_progress


@transaction.atomic
def recalculate_course_progress_by_enrollment_id(
    *,
    enrollment_id: int,
) -> CourseProgress:
    """
    Пересчитывает прогресс курса по идентификатору записи.
    """

    enrollment = get_course_enrollment_by_id(enrollment_id)

    return recalculate_course_progress(enrollment=enrollment)


def _calculate_progress_percent(
    *,
    completed_lessons_count: int,
    total_lessons_count: int,
) -> int:
    """
    Считает процент прохождения курса.
    """

    if total_lessons_count <= 0:
        return 0

    return round((completed_lessons_count / total_lessons_count) * 100)


def _sync_enrollment_progress(
    *,
    enrollment: CourseEnrollment,
    progress_percent: int,
) -> None:
    """
    Синхронизирует процент прогресса с записью на курс.
    """

    update_fields: list[str] = []

    if _model_has_field(CourseEnrollment, "progress_percent"):
        enrollment.progress_percent = progress_percent
        update_fields.append("progress_percent")

    if _model_has_field(CourseEnrollment, "last_activity_at"):
        enrollment.last_activity_at = timezone.now()
        update_fields.append("last_activity_at")

    if progress_percent >= 100:
        completed_status = getattr(
            CourseEnrollment.StatusChoices,
            "COMPLETED",
            "completed",
        )

        if _model_has_field(CourseEnrollment, "status"):
            enrollment.status = completed_status
            update_fields.append("status")

        if _model_has_field(CourseEnrollment, "completed_at"):
            enrollment.completed_at = enrollment.completed_at or timezone.now()
            update_fields.append("completed_at")

    if _model_has_field(CourseEnrollment, "updated_at"):
        update_fields.append("updated_at")

    if update_fields:
        enrollment.save(update_fields=update_fields)


def _get_lesson_progress_activity_ordering() -> list[str]:
    """
    Возвращает безопасную сортировку активности прогресса уроков.

    В текущей модели LessonProgress нет last_activity_at, поэтому
    используем ближайшие доступные поля.
    """

    ordering: list[str] = []

    for field_name in (
        "last_activity_at",
        "completed_at",
        "started_at",
        "updated_at",
        "created_at",
    ):
        if _model_has_field(LessonProgress, field_name):
            ordering.append(f"-{field_name}")

    ordering.append("-id")

    return ordering
