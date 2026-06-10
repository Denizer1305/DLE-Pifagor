from __future__ import annotations

from apps.course.models import Course
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_course_can_be_saved(
    *,
    course: Course,
) -> None:
    """
    Проверяет, что курс можно сохранить.
    """

    errors: dict[str, str] = {}

    if course.period_id and course.academic_year_id:
        if course.period.academic_year_id != course.academic_year_id:
            errors["period"] = _(
                "Учебный период должен относиться к учебному году курса."
            )

    if course.course_type == Course.CourseTypeChoices.ACADEMIC:
        if not course.organization_id:
            errors["organization"] = _("Для академического курса нужна организация.")

        if not course.subject_id:
            errors["subject"] = _("Для академического курса нужен предмет.")

        if not course.academic_year_id:
            errors["academic_year"] = _("Для академического курса нужен учебный год.")

        if not course.period_id:
            errors["period"] = _("Для академического курса нужен учебный период.")

    if course.visibility == Course.VisibilityChoices.PUBLIC_LINK:
        if course.allow_self_enrollment and not course.enrollment_code:
            errors["enrollment_code"] = _(
                "Для самостоятельной записи по публичной ссылке нужен код записи."
            )

    if errors:
        raise ValidationError(errors)
