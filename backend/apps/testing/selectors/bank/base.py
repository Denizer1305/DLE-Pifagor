from __future__ import annotations

from apps.testing.models import QuestionBankItem, QuestionBankOption


def bank_item_base_queryset():
    """
    Возвращает базовый queryset шаблонов вопросов.
    """

    return QuestionBankItem.objects.all()


def bank_item_detail_queryset():
    """
    Возвращает queryset шаблонов вопросов для детального просмотра.
    """

    return bank_item_base_queryset().prefetch_related("options")


def bank_option_base_queryset():
    """
    Возвращает базовый queryset вариантов шаблона вопроса.
    """

    return QuestionBankOption.objects.all()


def bank_option_detail_queryset():
    """
    Возвращает queryset вариантов шаблона вопроса для детального просмотра.
    """

    return bank_option_base_queryset()
