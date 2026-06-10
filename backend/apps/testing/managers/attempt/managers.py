from __future__ import annotations

from apps.testing.managers.attempt.querysets import TestAttemptQuerySet
from django.db import models


class TestAttemptManager(models.Manager.from_queryset(TestAttemptQuerySet)):
    """
    Менеджер попыток прохождения теста.
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
                "reviewer_teacher",
            )
        )
