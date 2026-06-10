from __future__ import annotations

from apps.testing.managers.test.querysets import TestQuerySet
from django.db import models


class TestManager(models.Manager.from_queryset(TestQuerySet)):
    """
    Менеджер тестов.
    """

    def get_queryset(self):
        """
        Возвращает queryset с базовой оптимизацией связей.
        """

        return (
            super()
            .get_queryset()
            .select_related(
                "course",
                "lesson",
                "lesson_block",
                "organization",
                "subject",
                "owner_teacher",
            )
        )
