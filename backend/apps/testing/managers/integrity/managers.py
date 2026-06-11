from __future__ import annotations

from django.db import models

from apps.testing.managers.integrity.querysets import (
    TestAttemptIntegrityReportQuerySet,
)


class TestAttemptIntegrityReportManager(
    models.Manager.from_queryset(TestAttemptIntegrityReportQuerySet)
):
    """
    Менеджер отчётов добросовестности прохождения теста.
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
            )
        )