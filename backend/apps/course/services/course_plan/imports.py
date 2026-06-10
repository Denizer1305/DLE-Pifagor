from __future__ import annotations

from typing import Any

from apps.course.models import CoursePlanImport
from apps.course.selectors import get_course_plan_import_by_id
from apps.course.services.course_plan.payloads import COURSE_PLAN_IMPORT_MUTABLE_FIELDS
from apps.course.services.course_plan.validation import (
    validate_course_plan_import_can_be_saved,
)
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def create_course_plan_import(
    *,
    data: dict[str, Any],
) -> CoursePlanImport:
    """
    Создаёт запись импорта КТП.
    """

    plan_import = CoursePlanImport()

    _apply_course_plan_import_data(
        plan_import=plan_import,
        data=data,
    )

    validate_course_plan_import_can_be_saved(plan_import=plan_import)

    plan_import.full_clean()
    plan_import.save()

    return plan_import


@transaction.atomic
def update_course_plan_import(
    *,
    plan_import: CoursePlanImport,
    data: dict[str, Any],
) -> CoursePlanImport:
    """
    Обновляет запись импорта КТП.
    """

    _apply_course_plan_import_data(
        plan_import=plan_import,
        data=data,
    )

    validate_course_plan_import_can_be_saved(plan_import=plan_import)

    plan_import.full_clean()
    plan_import.save()

    return plan_import


@transaction.atomic
def update_course_plan_import_by_id(
    *,
    import_id: int,
    data: dict[str, Any],
) -> CoursePlanImport:
    """
    Обновляет импорт КТП по идентификатору.
    """

    plan_import = get_course_plan_import_by_id(import_id)

    return update_course_plan_import(
        plan_import=plan_import,
        data=data,
    )


@transaction.atomic
def mark_course_plan_import_parsed(
    *,
    plan_import: CoursePlanImport,
    parsed_payload: dict[str, Any],
    parser_version: str = "",
) -> CoursePlanImport:
    """
    Помечает импорт КТП как разобранный.
    """

    plan_import.status = CoursePlanImport.StatusChoices.PARSED
    plan_import.parsed_payload = parsed_payload
    plan_import.errors = []
    plan_import.parser_version = parser_version or plan_import.parser_version

    plan_import.full_clean()
    plan_import.save(
        update_fields=[
            "status",
            "parsed_payload",
            "errors",
            "parser_version",
        ],
    )

    return plan_import


@transaction.atomic
def mark_course_plan_import_failed(
    *,
    plan_import: CoursePlanImport,
    errors: list,
) -> CoursePlanImport:
    """
    Помечает импорт КТП как ошибочный.
    """

    plan_import.status = CoursePlanImport.StatusChoices.FAILED
    plan_import.errors = errors

    plan_import.full_clean()
    plan_import.save(
        update_fields=[
            "status",
            "errors",
        ],
    )

    return plan_import


@transaction.atomic
def mark_course_plan_import_applied(
    *,
    plan_import: CoursePlanImport,
) -> CoursePlanImport:
    """
    Помечает импорт КТП как применённый.
    """

    plan_import.status = CoursePlanImport.StatusChoices.APPLIED
    plan_import.applied_at = timezone.now()

    plan_import.full_clean()
    plan_import.save(
        update_fields=[
            "status",
            "applied_at",
        ],
    )

    return plan_import


def _apply_course_plan_import_data(
    *,
    plan_import: CoursePlanImport,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к импорту КТП.
    """

    for field_name in COURSE_PLAN_IMPORT_MUTABLE_FIELDS:
        if field_name in data:
            setattr(plan_import, field_name, data[field_name])
