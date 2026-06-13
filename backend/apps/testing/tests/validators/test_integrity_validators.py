from __future__ import annotations

from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.testing.tests.factories import (
    create_integrity_report,
    create_risky_integrity_report,
)
from apps.testing.validators import (
    validate_integrity_report,
    validate_integrity_report_flags,
    validate_integrity_report_score,
)


class IntegrityReportValidatorsTestCase(TestCase):
    """
    Тесты валидаторов отчёта добросовестности.
    """

    def test_validate_integrity_report_allows_valid_report(self) -> None:
        """
        Валидный отчёт проходит проверку.
        """

        report = create_risky_integrity_report()

        validate_integrity_report(report=report)

    def test_validate_integrity_report_rejects_negative_score(self) -> None:
        """
        Риск не может быть отрицательным.
        """

        report = create_integrity_report()
        report.score = -1

        with self.assertRaises(ValidationError):
            validate_integrity_report_score(report=report)

    def test_validate_integrity_report_rejects_score_above_100(self) -> None:
        """
        Риск не может быть больше 100.
        """

        report = create_integrity_report()
        report.score = 101

        with self.assertRaises(ValidationError):
            validate_integrity_report_score(report=report)

    def test_validate_integrity_report_rejects_non_list_flags(self) -> None:
        """
        Признаки риска должны храниться списком.
        """

        report = create_integrity_report()
        report.flags_data = {
            "code": "too_fast_completion",
        }

        with self.assertRaises(ValidationError):
            validate_integrity_report_flags(report=report)

    def test_validate_integrity_report_rejects_non_dict_flag(self) -> None:
        """
        Каждый признак риска должен быть объектом.
        """

        report = create_integrity_report()
        report.flags_data = ["too_fast_completion"]

        with self.assertRaises(ValidationError):
            validate_integrity_report_flags(report=report)

    def test_validate_integrity_report_rejects_missing_flag_fields(self) -> None:
        """
        У признака риска должны быть обязательные поля.
        """

        report = create_integrity_report()
        report.flags_data = [
            {
                "code": "too_fast_completion",
            }
        ]

        with self.assertRaises(ValidationError):
            validate_integrity_report_flags(report=report)

    def test_validate_integrity_report_rejects_invalid_flag_weight(self) -> None:
        """
        Вес признака риска должен быть числом.
        """

        report = create_integrity_report()
        report.flags_data = [
            {
                "code": "too_fast_completion",
                "title": "Слишком быстрое прохождение",
                "description": "Попытка отправлена слишком быстро.",
                "weight": "25",
            }
        ]

        with self.assertRaises(ValidationError):
            validate_integrity_report_flags(report=report)