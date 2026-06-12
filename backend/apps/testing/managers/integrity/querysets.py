from __future__ import annotations

from apps.testing.constants import IntegrityRiskLevel
from django.db import models


class TestAttemptIntegrityReportQuerySet(models.QuerySet):
    """
    QuerySet отчётов добросовестности прохождения теста.
    """

    def for_attempt(self, attempt_id: int):
        """
        Фильтрует отчёты по попытке.
        """

        return self.filter(attempt_id=attempt_id)

    def for_test(self, test_id: int):
        """
        Фильтрует отчёты по тесту.
        """

        return self.filter(attempt__test_id=test_id)

    def for_learner(self, learner_id: int):
        """
        Фильтрует отчёты по обучающемуся.
        """

        return self.filter(attempt__learner_id=learner_id)

    def low_risk(self):
        """
        Возвращает отчёты с низким риском.
        """

        return self.filter(risk_level=IntegrityRiskLevel.LOW)

    def medium_risk(self):
        """
        Возвращает отчёты со средним риском.
        """

        return self.filter(risk_level=IntegrityRiskLevel.MEDIUM)

    def high_risk(self):
        """
        Возвращает отчёты с высоким риском.
        """

        return self.filter(risk_level=IntegrityRiskLevel.HIGH)

    def risky(self):
        """
        Возвращает отчёты со средним или высоким риском.
        """

        return self.filter(
            risk_level__in=[
                IntegrityRiskLevel.MEDIUM,
                IntegrityRiskLevel.HIGH,
            ]
        )
