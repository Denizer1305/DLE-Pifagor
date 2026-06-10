from __future__ import annotations

from pathlib import Path

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

ALLOWED_COURSE_PLAN_EXTENSIONS = {
    ".doc",
    ".docx",
    ".pdf",
}


def validate_course_plan_hours(
    *,
    total_hours: int,
    semester_hours: int,
    theory_hours: int,
    practice_hours: int,
    lab_hours: int,
    self_study_hours: int,
    consultation_hours: int,
) -> None:
    """
    Проверяет согласованность часов КТП.
    """

    errors: dict[str, str] = {}

    values = {
        "total_hours": total_hours,
        "semester_hours": semester_hours,
        "theory_hours": theory_hours,
        "practice_hours": practice_hours,
        "lab_hours": lab_hours,
        "self_study_hours": self_study_hours,
        "consultation_hours": consultation_hours,
    }

    for field_name, value in values.items():
        if value < 0:
            errors[field_name] = _("Количество часов не может быть отрицательным.")

    calculated_semester_hours = (
        theory_hours
        + practice_hours
        + lab_hours
        + self_study_hours
        + consultation_hours
    )

    if semester_hours and calculated_semester_hours > semester_hours:
        errors["semester_hours"] = _(
            "Сумма часов по видам работы не может превышать часы семестра."
        )

    if total_hours and semester_hours and semester_hours > total_hours:
        errors["semester_hours"] = _(
            "Часы семестра не могут превышать общее количество часов."
        )

    if errors:
        raise ValidationError(errors)


def validate_course_plan_file_extension(value) -> None:
    """
    Проверяет расширение файла КТП.
    """

    if not value:
        return

    filename = getattr(value, "name", str(value))
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_COURSE_PLAN_EXTENSIONS:
        raise ValidationError(
            _("КТП можно загрузить только в формате DOC, DOCX или PDF.")
        )


def validate_protocol_data(
    *,
    protocol_number: str,
    protocol_date,
) -> None:
    """
    Проверяет данные протокола рассмотрения КТП.
    """

    if bool(protocol_number) != bool(protocol_date):
        raise ValidationError(
            {
                "protocol_number": _(
                    "Номер и дата протокола должны быть заполнены вместе."
                )
            }
        )


def validate_approved_order_data(
    *,
    approved_order_number: str,
    approved_order_date,
) -> None:
    """
    Проверяет данные приказа утверждения КТП.
    """

    if bool(approved_order_number) != bool(approved_order_date):
        raise ValidationError(
            {
                "approved_order_number": _(
                    "Номер и дата приказа должны быть заполнены вместе."
                )
            }
        )
