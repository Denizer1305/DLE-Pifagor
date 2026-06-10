from __future__ import annotations

from typing import Any

from apps.course.models import CourseAccessRule
from apps.course.selectors import get_course_access_rule_by_id
from apps.course.services.course_access.payloads import (
    COURSE_ACCESS_RULE_MUTABLE_FIELDS,
)
from apps.course.services.course_access.validation import (
    validate_course_access_rule_can_be_saved,
)
from django.db import transaction


@transaction.atomic
def create_course_access_rule(
    *,
    data: dict[str, Any],
) -> CourseAccessRule:
    """
    Создаёт правило доступа к курсу.
    """

    access_rule = CourseAccessRule()

    _apply_course_access_rule_data(
        access_rule=access_rule,
        data=data,
    )

    validate_course_access_rule_can_be_saved(access_rule=access_rule)

    access_rule.full_clean()
    access_rule.save()

    return access_rule


@transaction.atomic
def update_course_access_rule(
    *,
    access_rule: CourseAccessRule,
    data: dict[str, Any],
) -> CourseAccessRule:
    """
    Обновляет правило доступа к курсу.
    """

    _apply_course_access_rule_data(
        access_rule=access_rule,
        data=data,
    )

    validate_course_access_rule_can_be_saved(access_rule=access_rule)

    access_rule.full_clean()
    access_rule.save()

    return access_rule


@transaction.atomic
def update_course_access_rule_by_id(
    *,
    rule_id: int,
    data: dict[str, Any],
) -> CourseAccessRule:
    """
    Обновляет правило доступа к курсу по идентификатору.
    """

    access_rule = get_course_access_rule_by_id(rule_id)

    return update_course_access_rule(
        access_rule=access_rule,
        data=data,
    )


@transaction.atomic
def deactivate_course_access_rule(
    *,
    access_rule: CourseAccessRule,
) -> CourseAccessRule:
    """
    Деактивирует правило доступа.
    """

    access_rule.is_active = False
    access_rule.full_clean()
    access_rule.save(
        update_fields=[
            "is_active",
            "updated_at",
        ],
    )

    return access_rule


@transaction.atomic
def restore_course_access_rule(
    *,
    access_rule: CourseAccessRule,
) -> CourseAccessRule:
    """
    Восстанавливает правило доступа.
    """

    access_rule.is_active = True
    access_rule.full_clean()
    access_rule.save(
        update_fields=[
            "is_active",
            "updated_at",
        ],
    )

    return access_rule


def _apply_course_access_rule_data(
    *,
    access_rule: CourseAccessRule,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к правилу доступа.
    """

    for field_name in COURSE_ACCESS_RULE_MUTABLE_FIELDS:
        if field_name in data:
            setattr(access_rule, field_name, data[field_name])
