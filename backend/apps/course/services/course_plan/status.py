from __future__ import annotations

from apps.course.models import CoursePlan
from apps.course.selectors import get_course_plan_by_id
from django.db import transaction


@transaction.atomic
def mark_course_plan_reviewed(
    *,
    plan: CoursePlan,
) -> CoursePlan:
    """
    Помечает КТП как проверенный.
    """

    plan.status = CoursePlan.StatusChoices.REVIEWED
    plan.full_clean()
    plan.save(
        update_fields=[
            "status",
            "updated_at",
        ],
    )

    return plan


@transaction.atomic
def mark_course_plan_reviewed_by_id(
    *,
    plan_id: int,
) -> CoursePlan:
    """
    Помечает КТП как проверенный по идентификатору.
    """

    plan = get_course_plan_by_id(plan_id)

    return mark_course_plan_reviewed(plan=plan)


@transaction.atomic
def approve_course_plan(
    *,
    plan: CoursePlan,
) -> CoursePlan:
    """
    Утверждает КТП.
    """

    plan.status = CoursePlan.StatusChoices.APPROVED
    plan.is_active = True
    plan.full_clean()
    plan.save(
        update_fields=[
            "status",
            "is_active",
            "updated_at",
        ],
    )

    return plan


@transaction.atomic
def approve_course_plan_by_id(
    *,
    plan_id: int,
) -> CoursePlan:
    """
    Утверждает КТП по идентификатору.
    """

    plan = get_course_plan_by_id(plan_id)

    return approve_course_plan(plan=plan)


@transaction.atomic
def archive_course_plan(
    *,
    plan: CoursePlan,
) -> CoursePlan:
    """
    Архивирует КТП.
    """

    plan.status = CoursePlan.StatusChoices.ARCHIVED
    plan.is_active = False
    plan.full_clean()
    plan.save(
        update_fields=[
            "status",
            "is_active",
            "updated_at",
        ],
    )

    return plan


@transaction.atomic
def archive_course_plan_by_id(
    *,
    plan_id: int,
) -> CoursePlan:
    """
    Архивирует КТП по идентификатору.
    """

    plan = get_course_plan_by_id(plan_id)

    return archive_course_plan(plan=plan)
