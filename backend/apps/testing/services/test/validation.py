from __future__ import annotations

from apps.testing.constants import TestStatus
from apps.testing.validators import validate_question_options_for_publish
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_test_can_be_published(*, test) -> None:
    """
    Проверяет, что тест можно опубликовать.
    """

    errors = {}

    if test.status == TestStatus.ARCHIVED:
        errors["status"] = _("Архивный тест нельзя опубликовать.")

    active_questions = test.questions.filter(is_active=True)

    if not active_questions.exists():
        errors["questions"] = _(
            "Перед публикацией добавьте хотя бы один активный вопрос."
        )

    if errors:
        raise ValidationError(errors)

    for question in active_questions:
        validate_question_options_for_publish(question=question)


def validate_test_can_be_archived(*, test) -> None:
    """
    Проверяет, что тест можно архивировать.
    """

    if test.status == TestStatus.ARCHIVED:
        raise ValidationError({"status": _("Тест уже находится в архиве.")})


def validate_test_can_be_restored(*, test) -> None:
    """
    Проверяет, что тест можно восстановить.
    """

    if test.status != TestStatus.ARCHIVED:
        raise ValidationError({"status": _("Восстановить можно только архивный тест.")})
