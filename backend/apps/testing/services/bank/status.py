from __future__ import annotations

from apps.testing.constants import BankItemStatus
from apps.testing.models import QuestionBankItem
from apps.testing.validators import (
    validate_bank_item_can_be_archived,
    validate_bank_item_can_be_published,
    validate_bank_item_can_be_restored,
)
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def publish_bank_item(*, bank_item: QuestionBankItem) -> QuestionBankItem:
    """
    Публикует шаблон вопроса.
    """

    validate_bank_item_can_be_published(item=bank_item)

    bank_item.status = BankItemStatus.PUBLISHED
    bank_item.is_active = True
    bank_item.published_at = timezone.now()
    bank_item.archived_at = None

    bank_item.full_clean()
    bank_item.save(
        update_fields=[
            "status",
            "is_active",
            "published_at",
            "archived_at",
            "updated_at",
        ]
    )

    return bank_item


@transaction.atomic
def archive_bank_item(*, bank_item: QuestionBankItem) -> QuestionBankItem:
    """
    Архивирует шаблон вопроса.
    """

    validate_bank_item_can_be_archived(item=bank_item)

    bank_item.status = BankItemStatus.ARCHIVED
    bank_item.is_active = False
    bank_item.archived_at = timezone.now()

    bank_item.full_clean()
    bank_item.save(
        update_fields=[
            "status",
            "is_active",
            "archived_at",
            "updated_at",
        ]
    )

    return bank_item


@transaction.atomic
def restore_bank_item(*, bank_item: QuestionBankItem) -> QuestionBankItem:
    """
    Восстанавливает шаблон вопроса в черновик.
    """

    validate_bank_item_can_be_restored(item=bank_item)

    bank_item.status = BankItemStatus.DRAFT
    bank_item.is_active = True
    bank_item.archived_at = None

    bank_item.full_clean()
    bank_item.save(
        update_fields=[
            "status",
            "is_active",
            "archived_at",
            "updated_at",
        ]
    )

    return bank_item
