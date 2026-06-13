from __future__ import annotations

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.testing.constants import (
    IntegrityRiskLevel,
    TestAttemptStatus,
)
from apps.testing.tests.factories import (
    create_attempt,
    create_integrity_report,
    create_risky_integrity_report,
    create_superadmin,
    create_teacher,
    create_test,
    extract_results,
)


class TeacherIntegrityReportApiTestCase(APITestCase):
    """
    API-тесты отчётов добросовестности в пространстве преподавателя.
    """

    def setUp(self) -> None:
        """
        Подготавливает базовые данные.
        """

        self.teacher = create_teacher()
        self.foreign_teacher = create_teacher()

        self.exam = create_test(owner_teacher=self.teacher)
        self.foreign_exam = create_test(owner_teacher=self.foreign_teacher)

        self.attempt = create_attempt(
            test=self.exam,
            status=TestAttemptStatus.SUBMITTED,
        )
        self.foreign_attempt = create_attempt(
            test=self.foreign_exam,
            status=TestAttemptStatus.SUBMITTED,
        )

        self.report = create_integrity_report(
            attempt=self.attempt,
            score=10,
            risk_level=IntegrityRiskLevel.LOW,
        )
        self.foreign_report = create_risky_integrity_report(
            attempt=self.foreign_attempt,
        )

    def test_teacher_can_get_own_integrity_reports_list(self) -> None:
        """
        Преподаватель видит отчёты только по своим тестам.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(
            reverse(
                "testing_teacher:"
                "testing-teacher-integrity-reports-list"
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        report_ids = {
            item["id"]
            for item in extract_results(response.json())
        }

        self.assertIn(self.report.id, report_ids)
        self.assertNotIn(self.foreign_report.id, report_ids)

    def test_teacher_can_get_integrity_report_detail(self) -> None:
        """
        Преподаватель получает детальный отчёт по своей попытке.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(
            reverse(
                "testing_teacher:"
                "testing-teacher-integrity-reports-detail",
                args=[self.report.id],
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], self.report.id)
        self.assertEqual(response.json()["attempt_id"], self.attempt.id)
        self.assertEqual(response.json()["risk_level"], IntegrityRiskLevel.LOW)

    def test_teacher_can_filter_integrity_reports_by_risk_level(self) -> None:
        """
        Преподаватель фильтрует отчёты по уровню риска.
        """

        risky_report = create_risky_integrity_report(
            attempt=create_attempt(
                test=self.exam,
                status=TestAttemptStatus.SUBMITTED,
            ),
        )

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(
            reverse(
                "testing_teacher:"
                "testing-teacher-integrity-reports-list"
            ),
            {
                "risk_level": IntegrityRiskLevel.HIGH,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        report_ids = {
            item["id"]
            for item in extract_results(response.json())
        }

        self.assertIn(risky_report.id, report_ids)
        self.assertNotIn(self.report.id, report_ids)

    def test_teacher_can_build_integrity_report_for_own_attempt(self) -> None:
        """
        Преподаватель формирует и сохраняет отчёт по своей попытке.
        """

        attempt = create_attempt(
            test=self.exam,
            status=TestAttemptStatus.SUBMITTED,
        )

        self.client.force_authenticate(user=self.teacher)

        response = self.client.post(
            reverse(
                "testing_teacher:"
                "testing-teacher-integrity-reports-build"
            ),
            {
                "attempt_id": attempt.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["attempt_id"], attempt.id)
        self.assertIn("score", response.json())
        self.assertIn("risk_level", response.json())
        self.assertIn("flags_data", response.json())

    def test_teacher_cannot_get_foreign_integrity_report_detail(self) -> None:
        """
        Преподаватель не получает отчёт чужого теста.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(
            reverse(
                "testing_teacher:"
                "testing-teacher-integrity-reports-detail",
                args=[self.foreign_report.id],
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_teacher_cannot_build_integrity_report_for_foreign_attempt(
        self,
    ) -> None:
        """
        Преподаватель не формирует отчёт по чужой попытке.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.post(
            reverse(
                "testing_teacher:"
                "testing-teacher-integrity-reports-build"
            ),
            {
                "attempt_id": self.foreign_attempt.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AdminIntegrityReportApiTestCase(APITestCase):
    """
    API-тесты отчётов добросовестности в административном пространстве.
    """

    def setUp(self) -> None:
        """
        Подготавливает базовые данные.
        """

        self.superadmin = create_superadmin()
        self.exam = create_test()
        self.attempt = create_attempt(
            test=self.exam,
            status=TestAttemptStatus.SUBMITTED,
        )
        self.report = create_risky_integrity_report(
            attempt=self.attempt,
        )

    def test_admin_can_get_integrity_reports_list(self) -> None:
        """
        Администратор получает список отчётов добросовестности.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse(
                "testing_admin:"
                "testing-admin-integrity-reports-list"
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        report_ids = {
            item["id"]
            for item in extract_results(response.json())
        }

        self.assertIn(self.report.id, report_ids)

    def test_admin_can_get_integrity_report_detail(self) -> None:
        """
        Администратор получает детальный отчёт.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse(
                "testing_admin:"
                "testing-admin-integrity-reports-detail",
                args=[self.report.id],
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], self.report.id)
        self.assertEqual(response.json()["attempt_id"], self.attempt.id)

    def test_admin_can_filter_integrity_reports_by_score(self) -> None:
        """
        Администратор фильтрует отчёты по баллу риска.
        """

        low_report = create_integrity_report(
            attempt=create_attempt(
                test=self.exam,
                status=TestAttemptStatus.SUBMITTED,
            ),
            score=5,
            risk_level=IntegrityRiskLevel.LOW,
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse(
                "testing_admin:"
                "testing-admin-integrity-reports-list"
            ),
            {
                "min_score": 50,
                "max_score": 100,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        report_ids = {
            item["id"]
            for item in extract_results(response.json())
        }

        self.assertIn(self.report.id, report_ids)
        self.assertNotIn(low_report.id, report_ids)

    def test_admin_can_build_integrity_report(self) -> None:
        """
        Администратор формирует и сохраняет отчёт по попытке.
        """

        attempt = create_attempt(
            test=self.exam,
            status=TestAttemptStatus.SUBMITTED,
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "testing_admin:"
                "testing-admin-integrity-reports-build"
            ),
            {
                "attempt_id": attempt.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["attempt_id"], attempt.id)
        self.assertIn("score", response.json())
        self.assertIn("risk_level", response.json())
        self.assertIn("flags_data", response.json())