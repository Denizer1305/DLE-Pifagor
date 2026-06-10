from __future__ import annotations

from apps.testing.managers.question.querysets import TestQuestionQuerySet
from django.db import models


class TestQuestionManager(models.Manager.from_queryset(TestQuestionQuerySet)):
    """
    Менеджер вопросов тестов.
    """

    def get_queryset(self):
        """
        Возвращает queryset с базовой оптимизацией.
        """

        return (
            super()
            .get_queryset()
            .select_related(
                "test",
                "test__course",
                "test__owner_teacher",
            )
        )
