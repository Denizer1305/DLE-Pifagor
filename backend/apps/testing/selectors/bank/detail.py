from __future__ import annotations

from apps.testing.selectors.bank.base import (
    bank_item_detail_queryset,
    bank_option_detail_queryset,
)
from django.shortcuts import get_object_or_404


def get_bank_item_by_id(bank_item_id: int):
    """
    Возвращает шаблон вопроса по идентификатору.
    """

    return get_object_or_404(
        bank_item_detail_queryset(),
        id=bank_item_id,
    )


def get_bank_item_for_update(bank_item_id: int):
    """
    Возвращает шаблон вопроса для изменения.
    """

    return get_object_or_404(
        bank_item_detail_queryset().select_for_update(),
        id=bank_item_id,
    )


def get_bank_option_by_id(bank_option_id: int):
    """
    Возвращает вариант шаблона вопроса по идентификатору.
    """

    return get_object_or_404(
        bank_option_detail_queryset(),
        id=bank_option_id,
    )


def get_bank_option_for_update(bank_option_id: int):
    """
    Возвращает вариант шаблона вопроса для изменения.
    """

    return get_object_or_404(
        bank_option_detail_queryset().select_for_update(),
        id=bank_option_id,
    )
