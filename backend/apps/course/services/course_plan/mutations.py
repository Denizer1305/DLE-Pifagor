from __future__ import annotations

from typing import Any

from apps.course.models import CoursePlan
from apps.course.selectors import get_course_plan_by_id
from apps.course.services.course_plan.payloads import COURSE_PLAN_MUTABLE_FIELDS
from apps.course.services.course_plan.validation import (
    validate_course_plan_can_be_saved,
)
from django.db import transaction


@transaction.atomic
def create_course_plan(
    *,
    data: dict[str, Any],
) -> CoursePlan:
    """
    Создаёт КТП курса.
    """

    plan = CoursePlan()

    _apply_course_plan_data(
        plan=plan,
        data=data,
    )

    validate_course_plan_can_be_saved(plan=plan)

    plan.full_clean()
    plan.save()

    return plan


@transaction.atomic
def update_course_plan(
    *,
    plan: CoursePlan,
    data: dict[str, Any],
) -> CoursePlan:
    """
    Обновляет КТП курса.
    """

    _apply_course_plan_data(
        plan=plan,
        data=data,
    )

    validate_course_plan_can_be_saved(plan=plan)

    plan.full_clean()
    plan.save()

    return plan


@transaction.atomic
def update_course_plan_by_id(
    *,
    plan_id: int,
    data: dict[str, Any],
) -> CoursePlan:
    """
    Обновляет КТП по идентификатору.
    """

    plan = get_course_plan_by_id(plan_id)

    return update_course_plan(
        plan=plan,
        data=data,
    )


def _apply_course_plan_data(
    *,
    plan: CoursePlan,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к КТП.
    """

    for field_name in COURSE_PLAN_MUTABLE_FIELDS:
        if field_name in data:
            setattr(plan, field_name, data[field_name])
