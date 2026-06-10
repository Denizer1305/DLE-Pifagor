from __future__ import annotations

from apps.course.models import CoursePlan, CoursePlanImport
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_course_plan_can_be_saved(
    *,
    plan: CoursePlan,
) -> None:
    """
    Проверяет, что КТП можно сохранить.
    """

    errors: dict[str, str] = {}

    hours_sum = (
        plan.theory_hours
        + plan.practice_hours
        + plan.lab_hours
        + plan.self_study_hours
        + plan.consultation_hours
    )

    if plan.total_hours and hours_sum > plan.total_hours:
        errors["total_hours"] = _(
            "Сумма часов по видам работ не может превышать общее количество часов."
        )

    if plan.semester_hours and plan.semester_hours > plan.total_hours:
        errors["semester_hours"] = _(
            "Часы семестра не могут превышать общее количество часов."
        )

    if errors:
        raise ValidationError(errors)


def validate_course_plan_import_can_be_saved(
    *,
    plan_import: CoursePlanImport,
) -> None:
    """
    Проверяет, что импорт КТП можно сохранить.
    """

    if not plan_import.course_plan_id:
        raise ValidationError({"course_plan": _("Для импорта нужно указать КТП.")})
