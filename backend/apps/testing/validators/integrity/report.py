from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_integrity_report(report) -> None:
    """
    Валидирует сохранённый отчёт добросовестности попытки.
    """

    validate_integrity_report_score(report=report)
    validate_integrity_report_flags(report=report)


def validate_integrity_report_score(report) -> None:
    """
    Проверяет итоговый риск отчёта.
    """

    if report.score < 0:
        raise ValidationError({"score": _("Риск не может быть отрицательным.")})

    if report.score > 100:
        raise ValidationError({"score": _("Риск не может быть больше 100.")})


def validate_integrity_report_flags(report) -> None:
    """
    Проверяет структуру признаков риска.
    """

    if report.flags_data in (None, ""):
        return

    if not isinstance(report.flags_data, list):
        raise ValidationError(
            {"flags_data": _("Признаки риска должны храниться списком.")}
        )

    for flag in report.flags_data:
        _validate_flag(flag=flag)


def _validate_flag(*, flag: dict) -> None:
    """
    Проверяет один признак риска.
    """

    if not isinstance(flag, dict):
        raise ValidationError(
            {"flags_data": _("Каждый признак риска должен быть объектом.")}
        )

    required_fields = {
        "code",
        "title",
        "description",
        "weight",
    }

    missing_fields = [
        field_name for field_name in required_fields if field_name not in flag
    ]

    if missing_fields:
        raise ValidationError(
            {"flags_data": _("У признака риска отсутствуют обязательные поля.")}
        )

    if not isinstance(flag["code"], str) or not flag["code"].strip():
        raise ValidationError(
            {"flags_data": _("Код признака риска должен быть строкой.")}
        )

    if not isinstance(flag["weight"], int):
        raise ValidationError(
            {"flags_data": _("Вес признака риска должен быть числом.")}
        )
