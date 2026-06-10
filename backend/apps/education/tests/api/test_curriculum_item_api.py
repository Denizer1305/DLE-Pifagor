from __future__ import annotations

from apps.education.models import CurriculumItem
from apps.education.tests.factories import (
    create_curriculum,
    create_curriculum_item,
    create_education_period,
    create_subject,
    create_user,
    extract_results,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class CurriculumItemApiTestCase(APITestCase):
    """
    Тесты API элементов учебного плана.
    """

    def setUp(self) -> None:
        self.superadmin = create_user(role_code="superadmin")
        self.curriculum = create_curriculum()
        self.period = create_education_period(
            academic_year=self.curriculum.academic_year,
        )
        self.subject = create_subject()
        self.curriculum_item = create_curriculum_item(
            curriculum=self.curriculum,
            period=self.period,
            subject=self.subject,
        )

    def test_superadmin_can_get_curriculum_items_list(self) -> None:
        """
        Глобальный администратор получает элементы учебного плана.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("education_admin:education-admin-curriculum-items-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = {item["id"] for item in extract_results(response.json())}
        self.assertIn(self.curriculum_item.id, ids)

    def test_filter_items_by_curriculum(self) -> None:
        """
        Фильтр curriculum_id ограничивает элементы учебного плана.
        """

        another_curriculum = create_curriculum()
        another_period = create_education_period(
            academic_year=another_curriculum.academic_year,
            code="another_period",
        )
        another_item = create_curriculum_item(
            curriculum=another_curriculum,
            period=another_period,
            subject=create_subject(code="another_subject"),
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("education_admin:education-admin-curriculum-items-list"),
            {
                "curriculum_id": self.curriculum.id,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.curriculum_item.id, ids)
        self.assertNotIn(another_item.id, ids)

    def test_superadmin_can_create_curriculum_item(self) -> None:
        """
        Глобальный администратор создаёт элемент учебного плана.
        """

        new_subject = create_subject(code="physics")

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("education_admin:education-admin-curriculum-items-list"),
            {
                "curriculum_id": self.curriculum.id,
                "period_id": self.period.id,
                "subject_id": new_subject.id,
                "sequence": 2,
                "planned_hours": 72,
                "contact_hours": 48,
                "independent_hours": 24,
                "assessment_type": CurriculumItem.AssessmentTypeChoices.EXAM,
                "is_required": True,
                "is_active": True,
                "notes": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_superadmin_can_deactivate_and_restore_curriculum_item(self) -> None:
        """
        Глобальный администратор деактивирует и восстанавливает элемент.
        """

        self.client.force_authenticate(user=self.superadmin)

        deactivate_response = self.client.post(
            reverse(
                "education_admin:education-admin-curriculum-items-deactivate",
                args=[self.curriculum_item.id],
            ),
        )

        self.assertEqual(deactivate_response.status_code, status.HTTP_200_OK)

        self.curriculum_item.refresh_from_db()
        self.assertFalse(self.curriculum_item.is_active)

        restore_response = self.client.post(
            reverse(
                "education_admin:education-admin-curriculum-items-restore",
                args=[self.curriculum_item.id],
            ),
        )

        self.assertEqual(restore_response.status_code, status.HTTP_200_OK)

        self.curriculum_item.refresh_from_db()
        self.assertTrue(self.curriculum_item.is_active)
