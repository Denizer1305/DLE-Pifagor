from __future__ import annotations

from apps.testing.managers.result.querysets import TestLearnerResultQuerySet
from django.db import models


class TestLearnerResultManager(models.Manager.from_queryset(TestLearnerResultQuerySet)):
    """
    Менеджер итоговых результатов обучающихся.
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
                "learner",
                "last_attempt",
            )
        )
