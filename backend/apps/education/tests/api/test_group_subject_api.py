from __future__ import annotations

from apps.education.models import GroupSubject
from apps.education.tests.factories import (
    create_curriculum,
    create_curriculum_item,
    create_education_period,
    create_group_subject,
    create_study_group,
    create_subject,
    create_user,
    extract_results,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class GroupSubjectApiTestCase(APITestCase):
    """
    Тесты API предметов учебных групп.
    """

    def setUp(self) -> None:
        self.superadmin = create_user(role_code="superadmin")
        self.group = create_study_group()
        self.subject = create_subject()
        self.academic_year = create_curriculum(
            organization=self.group.organization,
            department=self.group.department,
        ).academic_year
        self.period = create_education_period(
            academic_year=self.academic_year,
        )
        self.group_subject = create_group_subject(
            group=self.group,
            subject=self.subject,
            academic_year=self.academic_year,
            period=self.period,
        )

    def test_superadmin_can_get_group_subjects_list(self) -> None:
        """
        Глобальный администратор получает предметы групп.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("education_admin:education-admin-group-subjects-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = {item["id"] for item in extract_results(response.json())}
        self.assertIn(self.group_subject.id, ids)

    def test_superadmin_can_create_group_subject(self) -> None:
        """
        Глобальный администратор создаёт предмет группы.
        """

        new_subject = create_subject(code="informatics")

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("education_admin:education-admin-group-subjects-list"),
            {
                "group_id": self.group.id,
                "subject_id": new_subject.id,
                "academic_year_id": self.academic_year.id,
                "period_id": self.period.id,
                "planned_hours": 72,
                "contact_hours": 48,
                "independent_hours": 24,
                "assessment_type": GroupSubject.AssessmentTypeChoices.EXAM,
                "is_required": True,
                "is_active": True,
                "notes": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_superadmin_can_sync_group_subjects_from_curriculum(self) -> None:
        """
        Глобальный администратор создаёт предметы группы из учебного плана.
        """

        curriculum = create_curriculum(
            organization=self.group.organization,
            department=self.group.department,
        )
        period = create_education_period(
            academic_year=curriculum.academic_year,
            code="sync_period",
        )
        item = create_curriculum_item(
            curriculum=curriculum,
            period=period,
            subject=create_subject(code="sync_subject"),
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "education_admin:education-admin-group-subjects-sync-from-curriculum"
            ),
            {
                "curriculum_id": curriculum.id,
                "group_id": self.group.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["created"], 1)

        self.assertTrue(
            GroupSubject.objects.filter(
                group=self.group,
                subject=item.subject,
                period=period,
            ).exists()
        )

    def test_superadmin_can_deactivate_and_restore_group_subject(self) -> None:
        """
        Глобальный администратор деактивирует и восстанавливает предмет группы.
        """

        self.client.force_authenticate(user=self.superadmin)

        deactivate_response = self.client.post(
            reverse(
                "education_admin:education-admin-group-subjects-deactivate",
                args=[self.group_subject.id],
            ),
        )

        self.assertEqual(deactivate_response.status_code, status.HTTP_200_OK)

        self.group_subject.refresh_from_db()
        self.assertFalse(self.group_subject.is_active)

        restore_response = self.client.post(
            reverse(
                "education_admin:education-admin-group-subjects-restore",
                args=[self.group_subject.id],
            ),
        )

        self.assertEqual(restore_response.status_code, status.HTTP_200_OK)

        self.group_subject.refresh_from_db()
        self.assertTrue(self.group_subject.is_active)
