from __future__ import annotations

from apps.testing.constants import BankItemStatus
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_bank_item_can_be_copied_to_test(
    *,
    bank_item,
    test,
) -> None:
    """
    Проверяет, что шаблон вопроса можно скопировать в тест.
    """

    errors = {}

    if bank_item.status != BankItemStatus.PUBLISHED:
        errors["status"] = _("В тест можно добавить только опубликованный шаблон.")

    if not bank_item.is_active:
        errors["is_active"] = _("Неактивный шаблон нельзя добавить в тест.")

    if bank_item.organization_id != test.organization_id:
        errors["organization"] = _(
            "Шаблон должен относиться к той же организации, что и тест."
        )

    if bank_item.subject_id != test.subject_id:
        errors["subject"] = _(
            "Шаблон должен относиться к тому же предмету, что и тест."
        )

    if errors:
        raise ValidationError(errors)


def validate_bank_option_can_be_created(*, bank_item) -> None:
    """
    Проверяет, что к шаблону можно добавить вариант ответа.
    """

    if bank_item.status == BankItemStatus.ARCHIVED:
        raise ValidationError(
            {"bank_item": _("Нельзя добавлять варианты к архивному шаблону.")}
        )
