from __future__ import annotations

from apps.course.constants import (
    MAX_PROGRESS_PERCENT,
    MAX_SCORE_VALUE,
    MIN_PROGRESS_PERCENT,
    MIN_SCORE_VALUE,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_progress_percent(value: int) -> None:
    """
    Проверяет процент прогресса.
    """

    if value < MIN_PROGRESS_PERCENT or value > MAX_PROGRESS_PERCENT:
        raise ValidationError(_("Прогресс должен быть в диапазоне от 0 до 100."))


def validate_score_value(value: int | None) -> None:
    """
    Проверяет оценку / балл по уроку.
    """

    if value is None:
        return

    if value < MIN_SCORE_VALUE or value > MAX_SCORE_VALUE:
        raise ValidationError(_("Балл должен быть в диапазоне от 0 до 100."))


def validate_progress_dates(
    *,
    started_at,
    completed_at,
) -> None:
    """
    Проверяет даты начала и завершения прогресса.
    """

    if started_at and completed_at and completed_at < started_at:
        raise ValidationError(
            {"completed_at": _("Дата завершения не может быть раньше даты начала.")}
        )


def validate_lesson_progress_course_consistency(
    *,
    enrollment,
    lesson,
) -> None:
    """
    Проверяет, что прогресс урока относится к курсу зачисления.
    """

    if enrollment and lesson and lesson.course_id != enrollment.course_id:
        raise ValidationError(
            {"lesson": _("Урок должен относиться к тому же курсу, что и зачисление.")}
        )
