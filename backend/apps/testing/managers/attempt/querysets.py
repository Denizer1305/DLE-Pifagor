from __future__ import annotations

from apps.testing.constants import AttemptCheckStatus, TestAttemptStatus
from django.db import models


class TestAttemptQuerySet(models.QuerySet):
    """
    QuerySet попыток прохождения теста.
    """

    def for_test(self, test_id: int):
        """
        Фильтрует попытки по тесту.
        """

        return self.filter(test_id=test_id)

    def for_learner(self, learner_id: int):
        """
        Фильтрует попытки по обучающемуся.
        """

        return self.filter(learner_id=learner_id)

    def active(self):
        """
        Возвращает активные попытки.
        """

        return self.exclude(status=TestAttemptStatus.CANCELLED)

    def started(self):
        """
        Возвращает начатые попытки.
        """

        return self.filter(status=TestAttemptStatus.STARTED)

    def submitted(self):
        """
        Возвращает отправленные попытки.
        """

        return self.filter(status=TestAttemptStatus.SUBMITTED)

    def needs_review(self):
        """
        Возвращает попытки, ожидающие проверки преподавателем.
        """

        return self.filter(
            status=TestAttemptStatus.NEEDS_REVIEW,
            check_status=AttemptCheckStatus.NEEDS_REVIEW,
        )

    def auto_checked(self):
        """
        Возвращает автоматически проверенные попытки.
        """

        return self.filter(
            status=TestAttemptStatus.AUTO_CHECKED,
            check_status=AttemptCheckStatus.AUTO_CHECKED,
        )

    def confirmed(self):
        """
        Возвращает подтверждённые преподавателем попытки.
        """

        return self.filter(
            status__in=[
                TestAttemptStatus.CONFIRMED,
                TestAttemptStatus.PUBLISHED,
            ],
            is_confirmed_by_teacher=True,
        )

    def visible_to_learner(self):
        """
        Возвращает попытки, видимые обучающемуся.
        """

        return self.filter(is_visible_to_learner=True)

    def visible_to_guardian(self):
        """
        Возвращает попытки, видимые родителю.
        """

        return self.filter(is_visible_to_guardian=True)
