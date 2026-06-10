from __future__ import annotations

from apps.course.models import LessonProgress
from apps.course.selectors import get_lesson_progress_by_id
from apps.course.services.course_progress.ensure import (
    _get_lesson_status_value,
    _model_has_field,
    _save_model_fields,
)
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def start_lesson_progress(
    *,
    lesson_progress: LessonProgress,
) -> LessonProgress:
    """
    Переводит прогресс урока в состояние прохождения.
    """

    now = timezone.now()

    lesson_progress.status = _get_lesson_status_value(
        "IN_PROGRESS",
        "in_progress",
    )

    if _model_has_field(LessonProgress, "started_at"):
        lesson_progress.started_at = lesson_progress.started_at or now

    if _model_has_field(LessonProgress, "last_activity_at"):
        lesson_progress.last_activity_at = now

    _save_model_fields(
        lesson_progress,
        [
            "status",
            "started_at",
            "last_activity_at",
            "updated_at",
        ],
    )

    return lesson_progress


@transaction.atomic
def start_lesson_progress_by_id(
    *,
    progress_id: int,
) -> LessonProgress:
    """
    Запускает прогресс урока по идентификатору.
    """

    lesson_progress = get_lesson_progress_by_id(progress_id)

    return start_lesson_progress(lesson_progress=lesson_progress)


@transaction.atomic
def complete_lesson_progress(
    *,
    lesson_progress: LessonProgress,
) -> LessonProgress:
    """
    Завершает прогресс урока.
    """

    now = timezone.now()

    lesson_progress.status = _get_lesson_status_value(
        "COMPLETED",
        "completed",
    )

    if _model_has_field(LessonProgress, "started_at"):
        lesson_progress.started_at = lesson_progress.started_at or now

    if _model_has_field(LessonProgress, "completed_at"):
        lesson_progress.completed_at = lesson_progress.completed_at or now

    if _model_has_field(LessonProgress, "last_activity_at"):
        lesson_progress.last_activity_at = now

    if _model_has_field(LessonProgress, "progress_percent"):
        lesson_progress.progress_percent = 100

    _save_model_fields(
        lesson_progress,
        [
            "status",
            "started_at",
            "completed_at",
            "last_activity_at",
            "progress_percent",
            "updated_at",
        ],
    )

    return lesson_progress


@transaction.atomic
def complete_lesson_progress_by_id(
    *,
    progress_id: int,
) -> LessonProgress:
    """
    Завершает прогресс урока по идентификатору.
    """

    lesson_progress = get_lesson_progress_by_id(progress_id)

    return complete_lesson_progress(lesson_progress=lesson_progress)


@transaction.atomic
def reset_lesson_progress(
    *,
    lesson_progress: LessonProgress,
) -> LessonProgress:
    """
    Сбрасывает прогресс урока.
    """

    lesson_progress.status = _get_lesson_status_value(
        "NOT_STARTED",
        "not_started",
    )

    if _model_has_field(LessonProgress, "started_at"):
        lesson_progress.started_at = None

    if _model_has_field(LessonProgress, "completed_at"):
        lesson_progress.completed_at = None

    if _model_has_field(LessonProgress, "last_activity_at"):
        lesson_progress.last_activity_at = None

    if _model_has_field(LessonProgress, "progress_percent"):
        lesson_progress.progress_percent = 0

    _save_model_fields(
        lesson_progress,
        [
            "status",
            "started_at",
            "completed_at",
            "last_activity_at",
            "progress_percent",
            "updated_at",
        ],
    )

    return lesson_progress


@transaction.atomic
def reset_lesson_progress_by_id(
    *,
    progress_id: int,
) -> LessonProgress:
    """
    Сбрасывает прогресс урока по идентификатору.
    """

    lesson_progress = get_lesson_progress_by_id(progress_id)

    return reset_lesson_progress(lesson_progress=lesson_progress)
