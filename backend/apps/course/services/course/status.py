from __future__ import annotations

from apps.course.models import Course
from apps.course.selectors import get_course_by_id
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def publish_course(
    *,
    course: Course,
) -> Course:
    """
    Публикует курс.
    """

    course.status = Course.StatusChoices.PUBLISHED
    course.is_active = True

    if not course.published_at:
        course.published_at = timezone.now()

    course.full_clean()
    course.save(
        update_fields=[
            "status",
            "is_active",
            "published_at",
            "updated_at",
        ],
    )

    return course


@transaction.atomic
def publish_course_by_id(
    *,
    course_id: int,
) -> Course:
    """
    Публикует курс по идентификатору.
    """

    course = get_course_by_id(course_id)

    return publish_course(course=course)


@transaction.atomic
def archive_course(
    *,
    course: Course,
) -> Course:
    """
    Архивирует курс.
    """

    course.status = Course.StatusChoices.ARCHIVED
    course.is_active = False

    if not course.archived_at:
        course.archived_at = timezone.now()

    course.full_clean()
    course.save(
        update_fields=[
            "status",
            "is_active",
            "archived_at",
            "updated_at",
        ],
    )

    return course


@transaction.atomic
def archive_course_by_id(
    *,
    course_id: int,
) -> Course:
    """
    Архивирует курс по идентификатору.
    """

    course = get_course_by_id(course_id)

    return archive_course(course=course)


@transaction.atomic
def restore_course(
    *,
    course: Course,
) -> Course:
    """
    Восстанавливает курс в черновик.
    """

    course.status = Course.StatusChoices.DRAFT
    course.is_active = True
    course.archived_at = None

    course.full_clean()
    course.save(
        update_fields=[
            "status",
            "is_active",
            "archived_at",
            "updated_at",
        ],
    )

    return course


@transaction.atomic
def restore_course_by_id(
    *,
    course_id: int,
) -> Course:
    """
    Восстанавливает курс по идентификатору.
    """

    course = get_course_by_id(course_id)

    return restore_course(course=course)
