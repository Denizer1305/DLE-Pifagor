from __future__ import annotations

from apps.course.models import LessonProgress
from django.db.models import QuerySet


def lesson_progress_base_queryset() -> QuerySet[LessonProgress]:
    """
    Возвращает базовый queryset прогресса уроков.
    """

    return LessonProgress.objects.select_related(
        "enrollment",
        "course_progress",
        "lesson",
        "lesson__course",
        "lesson__section",
        "enrollment__learner",
    )


def lesson_progress_list_queryset(
    *,
    enrollment_id: int | None = None,
    course_progress_id: int | None = None,
    lesson_id: int | None = None,
    course_id: int | None = None,
    learner_id: int | None = None,
    status: str | None = None,
) -> QuerySet[LessonProgress]:
    """
    Возвращает список прогресса по урокам.
    """

    queryset = lesson_progress_base_queryset()

    if enrollment_id:
        queryset = queryset.filter(enrollment_id=enrollment_id)

    if course_progress_id:
        queryset = queryset.filter(course_progress_id=course_progress_id)

    if lesson_id:
        queryset = queryset.filter(lesson_id=lesson_id)

    if course_id:
        queryset = queryset.filter(enrollment__course_id=course_id)

    if learner_id:
        queryset = queryset.filter(enrollment__learner_id=learner_id)

    if status:
        queryset = queryset.filter(status=status)

    return queryset.order_by(
        "lesson__section__order",
        "lesson__order",
        "lesson__lesson_number",
    )


def lesson_progress_detail_queryset() -> QuerySet[LessonProgress]:
    """
    Возвращает queryset прогресса урока с деталями.
    """

    return lesson_progress_base_queryset()


def get_lesson_progress_by_id(
    progress_id: int,
) -> LessonProgress:
    """
    Возвращает прогресс урока по идентификатору.
    """

    return lesson_progress_detail_queryset().get(id=progress_id)


def get_lesson_progress_by_enrollment_and_lesson(
    *,
    enrollment_id: int,
    lesson_id: int,
) -> LessonProgress:
    """
    Возвращает прогресс конкретного урока по записи на курс.
    """

    return lesson_progress_detail_queryset().get(
        enrollment_id=enrollment_id,
        lesson_id=lesson_id,
    )
