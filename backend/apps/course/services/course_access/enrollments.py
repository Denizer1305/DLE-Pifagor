from __future__ import annotations

from typing import Any

from apps.course.models import CourseEnrollment
from apps.course.selectors import get_course_enrollment_by_id
from apps.course.services.course_access.payloads import COURSE_ENROLLMENT_MUTABLE_FIELDS
from apps.course.services.course_access.validation import (
    validate_course_enrollment_can_be_saved,
)
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def create_course_enrollment(
    *,
    data: dict[str, Any],
) -> CourseEnrollment:
    """
    Создаёт запись обучающегося на курс.
    """

    enrollment = CourseEnrollment()

    _apply_course_enrollment_data(
        enrollment=enrollment,
        data=data,
    )

    validate_course_enrollment_can_be_saved(enrollment=enrollment)

    enrollment.full_clean()
    enrollment.save()

    return enrollment


@transaction.atomic
def update_course_enrollment(
    *,
    enrollment: CourseEnrollment,
    data: dict[str, Any],
) -> CourseEnrollment:
    """
    Обновляет запись обучающегося на курс.
    """

    _apply_course_enrollment_data(
        enrollment=enrollment,
        data=data,
    )

    validate_course_enrollment_can_be_saved(enrollment=enrollment)

    enrollment.full_clean()
    enrollment.save()

    return enrollment


@transaction.atomic
def update_course_enrollment_by_id(
    *,
    enrollment_id: int,
    data: dict[str, Any],
) -> CourseEnrollment:
    """
    Обновляет запись на курс по идентификатору.
    """

    enrollment = get_course_enrollment_by_id(enrollment_id)

    return update_course_enrollment(
        enrollment=enrollment,
        data=data,
    )


@transaction.atomic
def start_course_enrollment(
    *,
    enrollment: CourseEnrollment,
) -> CourseEnrollment:
    """
    Переводит запись на курс в состояние прохождения.
    """

    enrollment.status = CourseEnrollment.StatusChoices.IN_PROGRESS
    enrollment.started_at = enrollment.started_at or timezone.now()
    enrollment.last_activity_at = timezone.now()

    enrollment.full_clean()
    enrollment.save(
        update_fields=[
            "status",
            "started_at",
            "last_activity_at",
            "updated_at",
        ],
    )

    return enrollment


@transaction.atomic
def complete_course_enrollment(
    *,
    enrollment: CourseEnrollment,
) -> CourseEnrollment:
    """
    Завершает прохождение курса.
    """

    now = timezone.now()

    enrollment.status = CourseEnrollment.StatusChoices.COMPLETED
    enrollment.started_at = enrollment.started_at or now
    enrollment.completed_at = enrollment.completed_at or now
    enrollment.last_activity_at = now
    enrollment.progress_percent = 100

    enrollment.full_clean()
    enrollment.save(
        update_fields=[
            "status",
            "started_at",
            "completed_at",
            "last_activity_at",
            "progress_percent",
            "updated_at",
        ],
    )

    return enrollment


@transaction.atomic
def cancel_course_enrollment(
    *,
    enrollment: CourseEnrollment,
) -> CourseEnrollment:
    """
    Отменяет запись на курс.
    """

    enrollment.status = CourseEnrollment.StatusChoices.CANCELLED
    enrollment.full_clean()
    enrollment.save(
        update_fields=[
            "status",
            "updated_at",
        ],
    )

    return enrollment


@transaction.atomic
def archive_course_enrollment(
    *,
    enrollment: CourseEnrollment,
) -> CourseEnrollment:
    """
    Архивирует запись на курс.
    """

    enrollment.status = CourseEnrollment.StatusChoices.ARCHIVED
    enrollment.full_clean()
    enrollment.save(
        update_fields=[
            "status",
            "updated_at",
        ],
    )

    return enrollment


def _apply_course_enrollment_data(
    *,
    enrollment: CourseEnrollment,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к записи на курс.
    """

    for field_name in COURSE_ENROLLMENT_MUTABLE_FIELDS:
        if field_name in data:
            setattr(enrollment, field_name, data[field_name])
