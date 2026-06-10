from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_test_structure(*, test) -> None:
    """
    Проверяет согласованность курса, урока и блока урока.
    """

    errors = {}

    _validate_lesson_belongs_to_course(
        test=test,
        errors=errors,
    )
    _validate_block_belongs_to_course_and_lesson(
        test=test,
        errors=errors,
    )
    _validate_course_context(
        test=test,
        errors=errors,
    )

    if errors:
        raise ValidationError(errors)


def _validate_lesson_belongs_to_course(*, test, errors: dict) -> None:
    """
    Проверяет, что урок относится к курсу теста.
    """

    if not test.lesson_id:
        return

    if test.lesson.course_id != test.course_id:
        errors["lesson"] = _("Урок должен относиться к выбранному курсу.")


def _validate_block_belongs_to_course_and_lesson(*, test, errors: dict) -> None:
    """
    Проверяет, что блок относится к курсу и выбранному уроку.
    """

    if not test.lesson_block_id:
        return

    block_lesson = test.lesson_block.lesson

    if block_lesson.course_id != test.course_id:
        errors["lesson_block"] = _("Блок урока должен относиться к выбранному курсу.")

    if test.lesson_id and block_lesson.id != test.lesson_id:
        errors["lesson_block"] = _("Блок должен относиться к выбранному уроку.")


def _validate_course_context(*, test, errors: dict) -> None:
    """
    Проверяет, что организация и предмет совпадают с курсом.
    """

    if not test.course_id:
        return

    if test.organization_id != test.course.organization_id:
        errors["organization"] = _(
            "Организация теста должна совпадать с организацией курса."
        )

    if test.subject_id != test.course.subject_id:
        errors["subject"] = _("Предмет теста должен совпадать с предметом курса.")
