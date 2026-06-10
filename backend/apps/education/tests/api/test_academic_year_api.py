from __future__ import annotations

from datetime import date

from apps.education.models import AcademicYear
from apps.education.tests.factories import (
    create_academic_year,
    create_user,
    extract_results,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AcademicYearApiTestCase(APITestCase):
    """
    Тесты API учебных годов.
    """

    def setUp(self) -> None:
        self.superadmin = create_user(role_code="superadmin")
        self.learner = create_user(role_code="learner")
        self.academic_year = create_academic_year()

    def test_superadmin_can_get_academic_years_list(self) -> None:
        """
        Глобальный администратор получает список учебных годов.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("education_admin:education-admin-academic-years-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        results = extract_results(response.json())
        ids = {item["id"] for item in results}

        self.assertIn(self.academic_year.id, ids)

    def test_anonymous_user_cannot_get_academic_years_list(self) -> None:
        """
        Анонимный пользователь не получает учебные годы.
        """

        response = self.client.get(
            reverse("education_admin:education-admin-academic-years-list")
        )

        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_learner_cannot_create_academic_year(self) -> None:
        """
        Обучающийся не может создать учебный год.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.post(
            reverse("education_admin:education-admin-academic-years-list"),
            {
                "name": "2026/2027",
                "start_date": "2026-09-01",
                "end_date": "2027-06-30",
                "description": "",
                "is_current": False,
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superadmin_can_create_academic_year(self) -> None:
        """
        Глобальный администратор создаёт учебный год.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("education_admin:education-admin-academic-years-list"),
            {
                "name": "2026/2027",
                "start_date": "2026-09-01",
                "end_date": "2027-06-30",
                "description": "Новый учебный год.",
                "is_current": False,
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(AcademicYear.objects.filter(name="2026/2027").exists())

    def test_superadmin_can_set_current_academic_year(self) -> None:
        """
        Глобальный администратор делает учебный год текущим.
        """

        old_year = create_academic_year(
            name="2024/2025",
            start_date=date(2024, 9, 1),
            end_date=date(2025, 6, 30),
            is_current=True,
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "education_admin:education-admin-academic-years-set-current",
                args=[self.academic_year.id],
            ),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.academic_year.refresh_from_db()
        old_year.refresh_from_db()

        self.assertTrue(self.academic_year.is_current)
        self.assertFalse(old_year.is_current)

    def test_superadmin_can_deactivate_and_restore_academic_year(self) -> None:
        """
        Глобальный администратор деактивирует и восстанавливает учебный год.
        """

        self.client.force_authenticate(user=self.superadmin)

        deactivate_response = self.client.post(
            reverse(
                "education_admin:education-admin-academic-years-deactivate",
                args=[self.academic_year.id],
            ),
        )

        self.assertEqual(deactivate_response.status_code, status.HTTP_200_OK)

        self.academic_year.refresh_from_db()
        self.assertFalse(self.academic_year.is_active)

        restore_response = self.client.post(
            reverse(
                "education_admin:education-admin-academic-years-restore",
                args=[self.academic_year.id],
            ),
        )

        self.assertEqual(restore_response.status_code, status.HTTP_200_OK)

        self.academic_year.refresh_from_db()
        self.assertTrue(self.academic_year.is_active)
