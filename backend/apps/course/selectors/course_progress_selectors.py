from __future__ import annotations

from apps.course.models import CourseProgress
from django.db.models import QuerySet


def course_progress_base_queryset() -> QuerySet[CourseProgress]:
    """
    Возвращает базовый queryset прогресса курса.
    """

    return CourseProgress.objects.select_related(
        "enrollment",
        "enrollment__course",
        "enrollment__learner",
        "last_lesson",
    )


def course_progress_list_queryset(
    *,
    enrollment_id: int | None = None,
    course_id: int | None = None,
    learner_id: int | None = None,
    completed: bool | None = None,
) -> QuerySet[CourseProgress]:
    """
    Возвращает список прогресса по курсам.
    """

    queryset = course_progress_base_queryset()

    if enrollment_id:
        queryset = queryset.filter(enrollment_id=enrollment_id)

    if course_id:
        queryset = queryset.filter(enrollment__course_id=course_id)

    if learner_id:
        queryset = queryset.filter(enrollment__learner_id=learner_id)

    if completed is True:
        queryset = queryset.filter(progress_percent=100)

    if completed is False:
        queryset = queryset.filter(progress_percent__lt=100)

    return queryset.order_by(
        "-last_activity_at",
        "-updated_at",
        "-id",
    )


def course_progress_detail_queryset() -> QuerySet[CourseProgress]:
    """
    Возвращает queryset прогресса курса с деталями.
    """

    return course_progress_base_queryset().prefetch_related(
        "lesson_progresses",
    )


def get_course_progress_by_id(
    progress_id: int,
) -> CourseProgress:
    """
    Возвращает прогресс курса по идентификатору.
    """

    return course_progress_detail_queryset().get(id=progress_id)


def get_course_progress_by_enrollment_id(
    enrollment_id: int,
) -> CourseProgress:
    """
    Возвращает прогресс курса по записи на курс.
    """

    return course_progress_detail_queryset().get(enrollment_id=enrollment_id)
