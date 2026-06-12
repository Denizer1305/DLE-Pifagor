from __future__ import annotations

from apps.testing.models import QuestionBankItem, QuestionBankOption
from apps.testing.services.bank.validation import validate_bank_option_can_be_created
from django.db import transaction


@transaction.atomic
def create_bank_item(*, data: dict) -> QuestionBankItem:
    """
    Создаёт шаблон вопроса в банке тестовых заданий.
    """

    bank_item = QuestionBankItem(**data)
    bank_item.full_clean()
    bank_item.save()

    return bank_item


@transaction.atomic
def update_bank_item(
    *,
    bank_item: QuestionBankItem,
    data: dict,
) -> QuestionBankItem:
    """
    Обновляет шаблон вопроса банка тестовых заданий.
    """

    for field_name, value in data.items():
        setattr(bank_item, field_name, value)

    bank_item.full_clean()
    bank_item.save()

    return bank_item


@transaction.atomic
def create_bank_option(*, data: dict) -> QuestionBankOption:
    """
    Создаёт вариант ответа шаблона вопроса.
    """

    bank_item = data["bank_item"]
    validate_bank_option_can_be_created(bank_item=bank_item)

    option = QuestionBankOption(**data)
    option.full_clean()
    option.save()

    return option


@transaction.atomic
def update_bank_option(
    *,
    option: QuestionBankOption,
    data: dict,
) -> QuestionBankOption:
    """
    Обновляет вариант ответа шаблона вопроса.
    """

    for field_name, value in data.items():
        setattr(option, field_name, value)

    option.full_clean()
    option.save()

    return option
