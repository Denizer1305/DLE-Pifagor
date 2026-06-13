from __future__ import annotations

from apps.testing.selectors import get_bank_item_for_update, get_test_by_id
from apps.testing.services.bank.duplication import duplicate_bank_item
from apps.testing.services.bank.import_to_test import copy_bank_item_to_test
from apps.testing.services.bank.status import (
    archive_bank_item,
    publish_bank_item,
    restore_bank_item,
)
from django.db import transaction


@transaction.atomic
def publish_bank_item_task(*, bank_item_id: int):
    """
    Публикует шаблон вопроса банка тестовых заданий.
    """

    bank_item = get_bank_item_for_update(bank_item_id)

    return publish_bank_item(bank_item=bank_item)


@transaction.atomic
def archive_bank_item_task(*, bank_item_id: int):
    """
    Архивирует шаблон вопроса банка тестовых заданий.
    """

    bank_item = get_bank_item_for_update(bank_item_id)

    return archive_bank_item(bank_item=bank_item)


@transaction.atomic
def restore_bank_item_task(*, bank_item_id: int):
    """
    Восстанавливает шаблон вопроса в черновик.
    """

    bank_item = get_bank_item_for_update(bank_item_id)

    return restore_bank_item(bank_item=bank_item)


@transaction.atomic
def duplicate_bank_item_task(
    *,
    bank_item_id: int,
    owner_teacher=None,
):
    """
    Создаёт копию шаблона вопроса.
    """

    bank_item = get_bank_item_for_update(bank_item_id)

    return duplicate_bank_item(
        bank_item=bank_item,
        owner_teacher=owner_teacher,
    )


@transaction.atomic
def copy_bank_item_to_test_task(
    *,
    bank_item_id: int,
    test_id: int,
    order: int | None = None,
):
    """
    Копирует шаблон вопроса в конкретный тест.
    """

    bank_item = get_bank_item_for_update(bank_item_id)
    test = get_test_by_id(test_id)

    return copy_bank_item_to_test(
        bank_item=bank_item,
        test=test,
        order=order,
    )
