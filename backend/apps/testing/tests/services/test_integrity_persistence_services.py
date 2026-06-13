from __future__ import annotations

from django.test import TestCase

from apps.testing.constants import IntegrityRiskLevel
from apps.testing.models import (
    TestAttemptIntegrityReport as IntegrityReportModel,
)
from apps.testing.services.integrity import (
    build_and_save_attempt_integrity_report,
    build_attempt_integrity_report_payload,
    calculate_integrity_risk_level,
    save_attempt_integrity_report,
)
from apps.testing.tests.factories import (
    create_attempt,
    create_risky_integrity_report,
)


class IntegrityPersistenceServicesTestCase(TestCase):
    """
    Тесты сервисов сохранения integrity report.
    """

    def test_calculate_integrity_risk_level_returns_low(self) -> None:
        """
        Низкий балл риска возвращает low.
        """

        self.assertEqual(
            calculate_integrity_risk_level(score=10),
            IntegrityRiskLevel.LOW,
        )

    def test_calculate_integrity_risk_level_returns_medium(self) -> None:
        """
        Средний балл риска возвращает medium.
        """

        self.assertEqual(
            calculate_integrity_risk_level(score=40),
            IntegrityRiskLevel.MEDIUM,
        )

    def test_calculate_integrity_risk_level_returns_high(self) -> None:
        """
        Высокий балл риска возвращает high.
        """

        self.assertEqual(
            calculate_integrity_risk_level(score=80),
            IntegrityRiskLevel.HIGH,
        )

    def test_build_attempt_integrity_report_payload_returns_structure(self) -> None:
        """
        Сервис формирует payload отчёта.
        """

        attempt = create_attempt()

        payload = build_attempt_integrity_report_payload(attempt=attempt)

        self.assertIn("score", payload)
        self.assertIn("risk_level", payload)
        self.assertIn("flags_data", payload)

    def test_save_attempt_integrity_report_creates_report(self) -> None:
        """
        Сервис создаёт сохранённый отчёт.
        """

        attempt = create_attempt()

        report = save_attempt_integrity_report(
            attempt=attempt,
            report_data={
                "score": 25,
                "risk_level": IntegrityRiskLevel.LOW,
                "flags_data": [],
            },
        )

        self.assertIsInstance(report, IntegrityReportModel)
        self.assertEqual(report.attempt, attempt)
        self.assertEqual(report.score, 25)

    def test_save_attempt_integrity_report_updates_existing_report(self) -> None:
        """
        Сервис обновляет существующий отчёт по попытке.
        """

        existing_report = create_risky_integrity_report()

        report = save_attempt_integrity_report(
            attempt=existing_report.attempt,
            report_data={
                "score": 10,
                "risk_level": IntegrityRiskLevel.LOW,
                "flags_data": [],
            },
        )

        self.assertEqual(report.id, existing_report.id)
        self.assertEqual(report.score, 10)
        self.assertEqual(report.risk_level, IntegrityRiskLevel.LOW)

    def test_build_and_save_attempt_integrity_report_creates_report(self) -> None:
        """
        Сервис формирует и сохраняет отчёт.
        """

        attempt = create_attempt()

        report = build_and_save_attempt_integrity_report(attempt=attempt)

        self.assertEqual(report.attempt, attempt)
        self.assertTrue(
            IntegrityReportModel.objects.filter(
                attempt=attempt,
            ).exists()
        )