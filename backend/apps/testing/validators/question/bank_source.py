from __future__ import annotations

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_question_bank_source(question) -> None:
    """
    Проверяет связь вопроса теста с шаблоном из банка заданий.
    """

    if question.source_bank_item_id is None:
        return

    bank_item = question.source_bank_item

    errors = {}

    if question.question_type != bank_item.question_type:
        errors["question_type"] = _("Тип вопроса должен совпадать с шаблоном из банка.")

    if question.check_mode != bank_item.check_mode:
        errors["check_mode"] = _("Режим проверки должен совпадать с шаблоном из банка.")

    if question.test.organization_id != bank_item.organization_id:
        errors["source_bank_item"] = _(
            "Шаблон вопроса должен относиться к той же организации, " "что и тест."
        )

    if question.test.subject_id != bank_item.subject_id:
        errors["subject"] = _(
            "Шаблон вопроса должен относиться к тому же предмету, " "что и тест."
        )

    if errors:
        raise ValidationError(errors)
