from __future__ import annotations

from apps.testing.managers.answer.querysets import TestAttemptAnswerQuerySet
from django.db import models


class TestAttemptAnswerManager(models.Manager.from_queryset(TestAttemptAnswerQuerySet)):
    """
    Менеджер ответов на вопросы теста.
    """

    def get_queryset(self):
        """
        Возвращает queryset с базовой оптимизацией.
        """

        return (
            super()
            .get_queryset()
            .select_related(
                "attempt",
                "attempt__test",
                "attempt__learner",
                "question",
                "selected_option",
            )
        )
