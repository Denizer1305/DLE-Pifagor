from __future__ import annotations

from apps.course.constants import (
    MAX_HOURS_VALUE,
    MAX_ORDER_VALUE,
    MIN_HOURS_VALUE,
    MIN_ORDER_VALUE,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_order_value(value: int) -> None:
    """
    Проверяет порядок элемента курса.
    """

    if value < MIN_ORDER_VALUE:
        raise ValidationError(_("Порядок должен быть положительным числом."))

    if value > MAX_ORDER_VALUE:
        raise ValidationError(_("Порядок элемента слишком большой."))


def validate_hours_value(value: int) -> None:
    """
    Проверяет количество часов.
    """

    if value < MIN_HOURS_VALUE:
        raise ValidationError(_("Количество часов не может быть отрицательным."))

    if value > MAX_HOURS_VALUE:
        raise ValidationError(_("Количество часов слишком большое."))


def validate_lesson_hours(
    *,
    planned_hours: int,
    theory_hours: int,
    practice_hours: int,
    lab_hours: int,
    self_study_hours: int,
) -> None:
    """
    Проверяет согласованность часов урока.
    """

    errors: dict[str, str] = {}

    values = {
        "planned_hours": planned_hours,
        "theory_hours": theory_hours,
        "practice_hours": practice_hours,
        "lab_hours": lab_hours,
        "self_study_hours": self_study_hours,
    }

    for field_name, value in values.items():
        if value < 0:
            errors[field_name] = _("Количество часов не может быть отрицательным.")

    calculated_hours = theory_hours + practice_hours + lab_hours + self_study_hours

    if planned_hours and calculated_hours > planned_hours:
        errors["planned_hours"] = _(
            "Сумма часов по видам работы не может превышать плановые часы урока."
        )

    if errors:
        raise ValidationError(errors)


def validate_material_link_placement(
    *,
    placement: str,
    section,
    lesson,
) -> None:
    """
    Проверяет размещение материала курса.
    """

    errors: dict[str, str] = {}

    if placement == "course":
        if section is not None or lesson is not None:
            errors["placement"] = _(
                "Материал уровня курса не должен быть привязан к разделу или уроку."
            )

    if placement == "section":
        if section is None:
            errors["section"] = _("Для материала раздела нужен раздел.")

        if lesson is not None:
            errors["lesson"] = _("Материал раздела не должен быть привязан к уроку.")

    if placement == "lesson" and lesson is None:
        errors["lesson"] = _("Для материала урока нужен урок.")

    if errors:
        raise ValidationError(errors)
