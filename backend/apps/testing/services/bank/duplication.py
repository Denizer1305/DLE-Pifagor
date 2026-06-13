from __future__ import annotations

from apps.testing.constants import BankItemStatus
from apps.testing.models import QuestionBankItem, QuestionBankOption
from apps.testing.services.bank.payloads import (
    build_bank_item_duplicate_payload,
    build_option_payload_from_bank_option,
)
from django.db import transaction


@transaction.atomic
def duplicate_bank_item(
    *,
    bank_item: QuestionBankItem,
    owner_teacher=None,
) -> QuestionBankItem:
    """
    Создаёт копию шаблона вопроса вместе с вариантами ответа.
    """

    duplicate_payload = build_bank_item_duplicate_payload(bank_item=bank_item)
    duplicate_payload.update(
        {
            "title": f"{bank_item.title} — копия",
            "status": BankItemStatus.DRAFT,
            "published_at": None,
            "archived_at": None,
        }
    )

    if owner_teacher is not None:
        duplicate_payload["owner_teacher"] = owner_teacher

    duplicate = QuestionBankItem(**duplicate_payload)
    duplicate.full_clean()
    duplicate.save()

    _duplicate_bank_options(
        source_bank_item=bank_item,
        target_bank_item=duplicate,
    )

    return duplicate


def _duplicate_bank_options(
    *,
    source_bank_item: QuestionBankItem,
    target_bank_item: QuestionBankItem,
) -> None:
    """
    Копирует варианты ответа между шаблонами.
    """

    for source_option in source_bank_item.options.order_by("order", "id"):
        option_payload = build_option_payload_from_bank_option(
            bank_option=source_option,
        )
        option_payload["bank_item"] = target_bank_item

        option = QuestionBankOption(**option_payload)
        option.full_clean()
        option.save()
