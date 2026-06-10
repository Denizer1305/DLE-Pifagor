from __future__ import annotations

from typing import Any

from apps.course.models import CourseGroupAccess
from apps.course.selectors import get_course_group_access_by_id
from apps.course.services.course_access.payloads import (
    COURSE_GROUP_ACCESS_MUTABLE_FIELDS,
)
from apps.course.services.course_access.validation import (
    validate_course_group_access_can_be_saved,
)
from django.db import transaction


@transaction.atomic
def create_course_group_access(
    *,
    data: dict[str, Any],
) -> CourseGroupAccess:
    """
    Создаёт доступ учебной группы к курсу.
    """

    group_access = CourseGroupAccess()

    _apply_course_group_access_data(
        group_access=group_access,
        data=data,
    )

    validate_course_group_access_can_be_saved(group_access=group_access)

    group_access.full_clean()
    group_access.save()

    return group_access


@transaction.atomic
def update_course_group_access(
    *,
    group_access: CourseGroupAccess,
    data: dict[str, Any],
) -> CourseGroupAccess:
    """
    Обновляет доступ учебной группы к курсу.
    """

    _apply_course_group_access_data(
        group_access=group_access,
        data=data,
    )

    validate_course_group_access_can_be_saved(group_access=group_access)

    group_access.full_clean()
    group_access.save()

    return group_access


@transaction.atomic
def update_course_group_access_by_id(
    *,
    access_id: int,
    data: dict[str, Any],
) -> CourseGroupAccess:
    """
    Обновляет доступ группы к курсу по идентификатору.
    """

    group_access = get_course_group_access_by_id(access_id)

    return update_course_group_access(
        group_access=group_access,
        data=data,
    )


@transaction.atomic
def show_course_for_group(
    *,
    group_access: CourseGroupAccess,
) -> CourseGroupAccess:
    """
    Делает курс видимым для группы.
    """

    group_access.visibility = CourseGroupAccess.VisibilityChoices.VISIBLE
    group_access.is_active = True
    group_access.full_clean()
    group_access.save(
        update_fields=[
            "visibility",
            "is_active",
            "updated_at",
        ],
    )

    return group_access


@transaction.atomic
def hide_course_for_group(
    *,
    group_access: CourseGroupAccess,
) -> CourseGroupAccess:
    """
    Скрывает курс от группы.
    """

    group_access.visibility = CourseGroupAccess.VisibilityChoices.HIDDEN
    group_access.full_clean()
    group_access.save(
        update_fields=[
            "visibility",
            "updated_at",
        ],
    )

    return group_access


@transaction.atomic
def archive_course_group_access(
    *,
    group_access: CourseGroupAccess,
) -> CourseGroupAccess:
    """
    Архивирует доступ группы к курсу.
    """

    group_access.visibility = CourseGroupAccess.VisibilityChoices.ARCHIVED
    group_access.is_active = False
    group_access.full_clean()
    group_access.save(
        update_fields=[
            "visibility",
            "is_active",
            "updated_at",
        ],
    )

    return group_access


def _apply_course_group_access_data(
    *,
    group_access: CourseGroupAccess,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к доступу группы.
    """

    for field_name in COURSE_GROUP_ACCESS_MUTABLE_FIELDS:
        if field_name in data:
            setattr(group_access, field_name, data[field_name])
