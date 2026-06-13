from __future__ import annotations

from apps.testing.constants import IntegrityRiskLevel
from apps.testing.selectors import (
    get_integrity_report_by_attempt_id,
    get_integrity_report_by_id,
    integrity_report_list_queryset,
    risky_integrity_report_list_queryset,
)
from apps.testing.tests.factories import (
    create_attempt,
    create_integrity_report,
    create_risky_integrity_report,
)
from django.test import TestCase


class IntegrityReportSelectorsTestCase(TestCase):
    """
    Тесты селекторов отчётов добросовестности.
    """

    def test_integrity_report_list_queryset_filters_by_attempt(self) -> None:
        """
        Селектор фильтрует отчёты по попытке.
        """

        attempt = create_attempt()
        foreign_attempt = create_attempt()

        report = create_integrity_report(attempt=attempt)
        foreign_report = create_integrity_report(attempt=foreign_attempt)

        queryset = integrity_report_list_queryset(attempt_id=attempt.id)

        self.assertIn(report, queryset)
        self.assertNotIn(foreign_report, queryset)

    def test_integrity_report_list_queryset_filters_by_test(self) -> None:
        """
        Селектор фильтрует отчёты по тесту.
        """

        attempt = create_attempt()
        foreign_attempt = create_attempt()

        report = create_integrity_report(attempt=attempt)
        foreign_report = create_integrity_report(attempt=foreign_attempt)

        queryset = integrity_report_list_queryset(test_id=attempt.test_id)

        self.assertIn(report, queryset)
        self.assertNotIn(foreign_report, queryset)

    def test_integrity_report_list_queryset_filters_by_learner(self) -> None:
        """
        Селектор фильтрует отчёты по обучающемуся.
        """

        attempt = create_attempt()
        foreign_attempt = create_attempt()

        report = create_integrity_report(attempt=attempt)
        foreign_report = create_integrity_report(attempt=foreign_attempt)

        queryset = integrity_report_list_queryset(
            learner_id=attempt.learner_id,
        )

        self.assertIn(report, queryset)
        self.assertNotIn(foreign_report, queryset)

    def test_integrity_report_list_queryset_filters_by_risk_level(self) -> None:
        """
        Селектор фильтрует отчёты по уровню риска.
        """

        high_report = create_risky_integrity_report()
        low_report = create_integrity_report(
            risk_level=IntegrityRiskLevel.LOW,
        )

        queryset = integrity_report_list_queryset(
            risk_level=IntegrityRiskLevel.HIGH,
        )

        self.assertIn(high_report, queryset)
        self.assertNotIn(low_report, queryset)

    def test_integrity_report_list_queryset_filters_by_score_range(self) -> None:
        """
        Селектор фильтрует отчёты по диапазону риска.
        """

        high_report = create_risky_integrity_report(score=80)
        low_report = create_integrity_report(score=10)

        queryset = integrity_report_list_queryset(
            min_score=50,
            max_score=100,
        )

        self.assertIn(high_report, queryset)
        self.assertNotIn(low_report, queryset)

    def test_risky_integrity_report_list_queryset_returns_risky_reports(
        self,
    ) -> None:
        """
        Селектор возвращает только отчёты со средним и высоким риском.
        """

        risky_report = create_risky_integrity_report()
        low_report = create_integrity_report(
            score=5,
            risk_level=IntegrityRiskLevel.LOW,
        )

        queryset = risky_integrity_report_list_queryset()

        self.assertIn(risky_report, queryset)
        self.assertNotIn(low_report, queryset)

    def test_get_integrity_report_by_id_returns_report(self) -> None:
        """
        Селектор возвращает отчёт по идентификатору.
        """

        report = create_integrity_report()

        found_report = get_integrity_report_by_id(report.id)

        self.assertEqual(found_report, report)

    def test_get_integrity_report_by_attempt_id_returns_report(self) -> None:
        """
        Селектор возвращает отчёт по идентификатору попытки.
        """

        attempt = create_attempt()
        report = create_integrity_report(attempt=attempt)

        found_report = get_integrity_report_by_attempt_id(attempt.id)

        self.assertEqual(found_report, report)
