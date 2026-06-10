from __future__ import annotations

from apps.education.models import Curriculum
from apps.education.tests.factories import (
    create_academic_year,
    create_curriculum,
    create_department,
    create_organization,
    create_user,
    extract_results,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CurriculumApiTestCase(APITestCase):
    """
    Тесты API учебных планов.
    """

    def setUp(self) -> None:
        self.superadmin = create_user(role_code="superadmin")
        self.learner = create_user(role_code="learner")
        self.organization = create_organization()
        self.department = create_department(organization=self.organization)
        self.academic_year = create_academic_year()
        self.curriculum = create_curriculum(
            organization=self.organization,
            department=self.department,
            academic_year=self.academic_year,
        )

    def test_superadmin_can_get_curricula_list(self) -> None:
        """
        Глобальный администратор получает список учебных планов.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("education_admin:education-admin-curricula-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = {item["id"] for item in extract_results(response.json())}
        self.assertIn(self.curriculum.id, ids)

    def test_filter_curricula_by_organization(self) -> None:
        """
        Фильтр organization_id ограничивает учебные планы.
        """

        another_organization = create_organization(name="Другая организация")
        another_curriculum = create_curriculum(
            organization=another_organization,
            department=create_department(organization=another_organization),
            academic_year=self.academic_year,
            code="another_curriculum",
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("education_admin:education-admin-curricula-list"),
            {
                "organization_id": self.organization.id,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.curriculum.id, ids)
        self.assertNotIn(another_curriculum.id, ids)

    def test_learner_cannot_create_curriculum(self) -> None:
        """
        Обучающийся не создаёт учебный план.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.post(
            reverse("education_admin:education-admin-curricula-list"),
            {
                "organization_id": self.organization.id,
                "department_id": self.department.id,
                "academic_year_id": self.academic_year.id,
                "code": "blocked_curriculum",
                "name": "Запрещённый учебный план",
                "description": "",
                "total_hours": 144,
                "status": Curriculum.StatusChoices.DRAFT,
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superadmin_can_create_curriculum(self) -> None:
        """
        Глобальный администратор создаёт учебный план.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("education_admin:education-admin-curricula-list"),
            {
                "organization_id": self.organization.id,
                "department_id": self.department.id,
                "academic_year_id": self.academic_year.id,
                "code": "new_curriculum",
                "name": "Новый учебный план",
                "description": "",
                "total_hours": 144,
                "status": Curriculum.StatusChoices.DRAFT,
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Curriculum.objects.filter(code="new_curriculum").exists())

    def test_superadmin_can_activate_archive_and_restore_curriculum(self) -> None:
        """
        Глобальный администратор управляет статусом учебного плана.
        """

        self.client.force_authenticate(user=self.superadmin)

        activate_response = self.client.post(
            reverse(
                "education_admin:education-admin-curricula-activate",
                args=[self.curriculum.id],
            ),
        )

        self.assertEqual(activate_response.status_code, status.HTTP_200_OK)

        self.curriculum.refresh_from_db()
        self.assertEqual(self.curriculum.status, Curriculum.StatusChoices.ACTIVE)

        archive_response = self.client.post(
            reverse(
                "education_admin:education-admin-curricula-archive",
                args=[self.curriculum.id],
            ),
        )

        self.assertEqual(archive_response.status_code, status.HTTP_200_OK)

        self.curriculum.refresh_from_db()
        self.assertEqual(
            self.curriculum.status,
            Curriculum.StatusChoices.ARCHIVED,
        )
        self.assertFalse(self.curriculum.is_active)

        restore_response = self.client.post(
            reverse(
                "education_admin:education-admin-curricula-restore",
                args=[self.curriculum.id],
            ),
        )

        self.assertEqual(restore_response.status_code, status.HTTP_200_OK)

        self.curriculum.refresh_from_db()
        self.assertEqual(self.curriculum.status, Curriculum.StatusChoices.DRAFT)
        self.assertTrue(self.curriculum.is_active)
