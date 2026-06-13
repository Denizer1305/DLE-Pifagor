from __future__ import annotations

from django.test import TestCase

from apps.testing.constants import IntegrityRiskLevel
from apps.testing.models import (
    TestAttemptIntegrityReport as IntegrityReportModel,
)
from apps.testing.tests.factories import (
    create_attempt,
    create_integrity_report,
    create_risky_integrity_report,
)


class IntegrityReportModelsTestCase(TestCase):
    """
    Smoke-тесты модели отчёта добросовестности попытки.
    """

    def test_create_integrity_report(self) -> None:
        """
        Отчёт добросовестности создаётся корректно.
        """

        attempt = create_attempt()
        report = create_integrity_report(
            attempt=attempt,
            score=0,
            risk_level=IntegrityRiskLevel.LOW,
            flags_data=[],
        )

        self.assertIsInstance(report, IntegrityReportModel)
        self.assertEqual(report.attempt, attempt)
        self.assertEqual(report.score, 0)
        self.assertEqual(report.risk_level, IntegrityRiskLevel.LOW)
        self.assertEqual(report.flags_data, [])
        self.assertIn(str(attempt), str(report))

    def test_create_risky_integrity_report(self) -> None:
        """
        Фабрика создаёт отчёт с высоким риском.
        """

        report = create_risky_integrity_report()

        self.assertEqual(report.risk_level, IntegrityRiskLevel.HIGH)
        self.assertGreaterEqual(report.score, 70)
        self.assertTrue(report.flags_data)

    def test_integrity_report_full_clean_for_valid_object(self) -> None:
        """
        Валидный отчёт проходит full_clean.
        """

        report = create_risky_integrity_report()

        report.full_clean()

    def test_integrity_report_has_one_to_one_attempt_relation(self) -> None:
        """
        У попытки есть один сохранённый integrity report.
        """

        attempt = create_attempt()
        report = create_integrity_report(attempt=attempt)

        self.assertEqual(attempt.integrity_report, report)

    def test_integrity_report_str_contains_attempt_and_risk_level(self) -> None:
        """
        __str__ отчёта содержит попытку и уровень риска.
        """

        report = create_integrity_report(
            risk_level=IntegrityRiskLevel.MEDIUM,
        )

        self.assertIn(str(report.attempt), str(report))
        self.assertIn(IntegrityRiskLevel.MEDIUM, str(report))