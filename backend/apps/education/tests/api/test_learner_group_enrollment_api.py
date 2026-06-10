from __future__ import annotations

from apps.education.models import LearnerGroupEnrollment
from apps.education.tests.factories import (
    create_academic_year,
    create_learner_group_enrollment,
    create_study_group,
    create_user,
    extract_results,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class LearnerGroupEnrollmentApiTestCase(APITestCase):
    """
    Тесты API академических зачислений.
    """

    def setUp(self) -> None:
        self.superadmin = create_user(role_code="superadmin")
        self.learner = create_user(
            role_code="learner",
            first_name="Анна",
            last_name="Иванова",
        )
        self.group = create_study_group()
        self.academic_year = create_academic_year()
        self.enrollment = create_learner_group_enrollment(
            learner=self.learner,
            group=self.group,
            academic_year=self.academic_year,
            journal_number=1,
        )

    def test_superadmin_can_get_enrollments_list(self) -> None:
        """
        Глобальный администратор получает список зачислений.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("education_admin:education-admin-learner-enrollments-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = {item["id"] for item in extract_results(response.json())}
        self.assertIn(self.enrollment.id, ids)

    def test_learner_sees_own_enrollment(self) -> None:
        """
        Обучающийся видит своё зачисление.
        """

        other_learner = create_user(role_code="learner")
        other_enrollment = create_learner_group_enrollment(
            learner=other_learner,
            group=self.group,
            academic_year=self.academic_year,
            journal_number=2,
            is_primary=False,
        )

        self.client.force_authenticate(user=self.learner)

        response = self.client.get(
            reverse("education_admin:education-admin-learner-enrollments-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.enrollment.id, ids)
        self.assertNotIn(other_enrollment.id, ids)

    def test_superadmin_can_create_enrollment(self) -> None:
        """
        Глобальный администратор создаёт академическое зачисление.
        """

        learner = create_user(role_code="learner")

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("education_admin:education-admin-learner-enrollments-list"),
            {
                "learner_id": learner.id,
                "group_id": self.group.id,
                "academic_year_id": self.academic_year.id,
                "enrollment_date": str(self.academic_year.start_date),
                "completion_date": None,
                "status": LearnerGroupEnrollment.StatusChoices.ACTIVE,
                "is_primary": True,
                "journal_number": 3,
                "notes": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_superadmin_can_complete_enrollment(self) -> None:
        """
        Глобальный администратор завершает зачисление.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "education_admin:education-admin-learner-enrollments-complete",
                args=[self.enrollment.id],
            ),
            {
                "completion_date": str(self.academic_year.end_date),
                "status": LearnerGroupEnrollment.StatusChoices.GRADUATED,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.enrollment.refresh_from_db()
        self.assertEqual(
            self.enrollment.status,
            LearnerGroupEnrollment.StatusChoices.GRADUATED,
        )
        self.assertFalse(self.enrollment.is_primary)

    def test_superadmin_can_assign_missing_journal_numbers(self) -> None:
        """
        Глобальный администратор назначает недостающие номера в журнале.
        """

        learner = create_user(role_code="learner")
        enrollment = create_learner_group_enrollment(
            learner=learner,
            group=self.group,
            academic_year=self.academic_year,
            journal_number=None,
            is_primary=False,
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "education_admin:education-admin-learner-enrollments-assign-journal-numbers"
            ),
            {
                "group_id": self.group.id,
                "academic_year_id": self.academic_year.id,
                "start_number": 1,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        enrollment.refresh_from_db()
        self.assertIsNotNone(enrollment.journal_number)
