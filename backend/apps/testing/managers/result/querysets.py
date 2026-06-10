from __future__ import annotations

from apps.testing.constants import LearnerResultStatus
from django.db import models


class TestLearnerResultQuerySet(models.QuerySet):
    """
    QuerySet итоговых результатов обучающихся по тестам.
    """

    def for_test(self, test_id: int):
        """
        Фильтрует результаты по тесту.
        """

        return self.filter(test_id=test_id)

    def for_learner(self, learner_id: int):
        """
        Фильтрует результаты по обучающемуся.
        """

        return self.filter(learner_id=learner_id)

    def active(self):
        """
        Возвращает активные результаты.
        """

        return self.filter(status=LearnerResultStatus.ACTIVE)

    def blocked(self):
        """
        Возвращает заблокированные результаты.
        """

        return self.filter(
            status=LearnerResultStatus.BLOCKED,
            is_blocked=True,
        )

    def archived(self):
        """
        Возвращает архивные результаты.
        """

        return self.filter(status=LearnerResultStatus.ARCHIVED)

    def visible_to_learner(self):
        """
        Возвращает результаты, видимые обучающемуся.
        """

        return self.filter(is_visible_to_learner=True)

    def visible_to_guardian(self):
        """
        Возвращает результаты, видимые родителю.
        """

        return self.filter(is_visible_to_guardian=True)

    def passed(self):
        """
        Возвращает результаты с пройденным тестом.
        """

        return self.filter(is_passed=True)
