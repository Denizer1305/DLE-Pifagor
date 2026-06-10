from __future__ import annotations

from typing import Any

from apps.course.models import Course
from apps.course.services.course.mutations import create_course
from apps.course.services.course_plan.mutations import create_course_plan
from django.db import transaction


@transaction.atomic
def create_course_with_plan(
    *,
    course_data: dict[str, Any],
    plan_data: dict[str, Any],
) -> Course:
    """
    Создаёт курс вместе с КТП.
    """

    course = create_course(data=course_data)

    create_course_plan(
        data={
            **plan_data,
            "course": course,
        },
    )

    return course
