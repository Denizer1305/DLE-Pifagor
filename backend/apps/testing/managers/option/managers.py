from __future__ import annotations

from apps.testing.managers.option.querysets import TestQuestionOptionQuerySet
from django.db import models


class TestQuestionOptionManager(
    models.Manager.from_queryset(TestQuestionOptionQuerySet)
):
    """
    Менеджер вариантов ответа.
    """

    def get_queryset(self):
        """
        Возвращает queryset с базовой оптимизацией.
        """

        return (
            super()
            .get_queryset()
            .select_related(
                "question",
                "question__test",
            )
        )
