from __future__ import annotations

from apps.testing.managers.bank.querysets import (
    QuestionBankItemQuerySet,
    QuestionBankOptionQuerySet,
)
from django.db import models


class QuestionBankItemManager(models.Manager.from_queryset(QuestionBankItemQuerySet)):
    """
    Менеджер шаблонов вопросов банка тестовых заданий.
    """

    def get_queryset(self):
        """
        Возвращает queryset с базовой оптимизацией.
        """

        return (
            super()
            .get_queryset()
            .select_related(
                "organization",
                "subject",
                "owner_teacher",
            )
        )


class QuestionBankOptionManager(
    models.Manager.from_queryset(QuestionBankOptionQuerySet)
):
    """
    Менеджер вариантов ответа шаблона вопроса.
    """

    def get_queryset(self):
        """
        Возвращает queryset с базовой оптимизацией.
        """

        return (
            super()
            .get_queryset()
            .select_related(
                "bank_item",
                "bank_item__organization",
                "bank_item__subject",
                "bank_item__owner_teacher",
            )
        )
