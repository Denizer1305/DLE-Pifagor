from __future__ import annotations

from apps.education.models import EducationPeriod
from apps.education.tests.factories import (
    create_academic_year,
    create_education_period,
    create_user,
    extract_results,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class EducationPeriodApiTestCase(APITestCase):
    """
    Тесты API учебных периодов.
    """

    def setUp(self) -> None:
        self.superadmin = create_user(role_code="superadmin")
        self.learner = create_user(role_code="learner")
        self.academic_year = create_academic_year()
        self.period = create_education_period(
            academic_year=self.academic_year,
        )

    def test_superadmin_can_get_periods_list(self) -> None:
        """
        Глобальный администратор получает список периодов.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("education_admin:education-admin-periods-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = {item["id"] for item in extract_results(response.json())}
        self.assertIn(self.period.id, ids)

    def test_filter_periods_by_academic_year(self) -> None:
        """
        Фильтр academic_year_id ограничивает периоды учебным годом.
        """

        second_year = create_academic_year(
            name="2026/2027",
            start_date="2026-09-01",
            end_date="2027-06-30",
        )
        another_period = create_education_period(
            academic_year=second_year,
            code="second_year_period",
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("education_admin:education-admin-periods-list"),
            {
                "academic_year_id": self.academic_year.id,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.period.id, ids)
        self.assertNotIn(another_period.id, ids)

    def test_learner_cannot_create_period(self) -> None:
        """
        Обучающийся не создаёт учебный период.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.post(
            reverse("education_admin:education-admin-periods-list"),
            {
                "academic_year_id": self.academic_year.id,
                "name": "2 семестр",
                "code": "semester_2",
                "period_type": EducationPeriod.PeriodTypeChoices.SEMESTER,
                "sequence": 2,
                "start_date": f"{self.academic_year.end_date.year}-01-10",
                "end_date": str(self.academic_year.end_date),
                "description": "",
                "is_current": False,
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superadmin_can_create_period(self) -> None:
        """
        Глобальный администратор создаёт период.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("education_admin:education-admin-periods-list"),
            {
                "academic_year_id": self.academic_year.id,
                "name": "2 семестр",
                "code": "semester_2",
                "period_type": EducationPeriod.PeriodTypeChoices.SEMESTER,
                "sequence": 2,
                "start_date": f"{self.academic_year.end_date.year}-01-10",
                "end_date": str(self.academic_year.end_date),
                "description": "",
                "is_current": False,
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(EducationPeriod.objects.filter(code="semester_2").exists())

    def test_superadmin_can_set_current_period(self) -> None:
        """
        Глобальный администратор делает период текущим.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "education_admin:education-admin-periods-set-current",
                args=[self.period.id],
            ),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.period.refresh_from_db()
        self.assertTrue(self.period.is_current)
