from __future__ import annotations

from apps.education.models import TeacherGroupSubject
from apps.education.tests.factories import (
    create_group_subject,
    create_teacher_group_subject,
    create_teacher_organization,
    create_teacher_subject,
    create_user,
    extract_results,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TeacherGroupSubjectApiTestCase(APITestCase):
    """
    Тесты API назначений преподавателей.
    """

    def setUp(self) -> None:
        self.superadmin = create_user(role_code="superadmin")
        self.teacher = create_user(
            role_code="teacher",
            first_name="Иван",
            last_name="Петров",
        )
        self.group_subject = create_group_subject()

        create_teacher_organization(
            teacher=self.teacher,
            organization=self.group_subject.group.organization,
        )
        create_teacher_subject(
            teacher=self.teacher,
            subject=self.group_subject.subject,
        )

        self.assignment = create_teacher_group_subject(
            teacher=self.teacher,
            group_subject=self.group_subject,
            planned_hours=36,
        )

    def test_superadmin_can_get_teacher_assignments_list(self) -> None:
        """
        Глобальный администратор получает назначения преподавателей.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("education_admin:education-admin-teacher-group-subjects-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        ids = {item["id"] for item in extract_results(response.json())}
        self.assertIn(self.assignment.id, ids)

    def test_superadmin_can_create_teacher_assignment(self) -> None:
        """
        Глобальный администратор создаёт назначение преподавателя.
        """

        another_teacher = create_user(
            role_code="teacher",
            first_name="Пётр",
            last_name="Сидоров",
        )

        create_teacher_organization(
            teacher=another_teacher,
            organization=self.group_subject.group.organization,
        )
        create_teacher_subject(
            teacher=another_teacher,
            subject=self.group_subject.subject,
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("education_admin:education-admin-teacher-group-subjects-list"),
            {
                "teacher_id": another_teacher.id,
                "group_subject_id": self.group_subject.id,
                "role": TeacherGroupSubject.RoleChoices.ASSISTANT,
                "is_primary": False,
                "is_active": True,
                "planned_hours": 12,
                "starts_at": str(self.group_subject.period.start_date),
                "ends_at": str(self.group_subject.period.end_date),
                "notes": "",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_superadmin_can_deactivate_and_restore_teacher_assignment(self) -> None:
        """
        Глобальный администратор деактивирует и восстанавливает назначение.
        """

        self.client.force_authenticate(user=self.superadmin)

        deactivate_response = self.client.post(
            reverse(
                "education_admin:education-admin-teacher-group-subjects-deactivate",
                args=[self.assignment.id],
            ),
        )

        self.assertEqual(deactivate_response.status_code, status.HTTP_200_OK)

        self.assignment.refresh_from_db()
        self.assertFalse(self.assignment.is_active)

        restore_response = self.client.post(
            reverse(
                "education_admin:education-admin-teacher-group-subjects-restore",
                args=[self.assignment.id],
            ),
        )

        self.assertEqual(restore_response.status_code, status.HTTP_200_OK)

        self.assignment.refresh_from_db()
        self.assertTrue(self.assignment.is_active)

    def test_superadmin_can_set_primary_teacher_assignment(self) -> None:
        """
        Глобальный администратор делает назначение основным.
        """

        self.assignment.is_primary = False
        self.assignment.role = TeacherGroupSubject.RoleChoices.ASSISTANT
        self.assignment.save(update_fields=["is_primary", "role"])

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "education_admin:education-admin-teacher-group-subjects-set-primary",
                args=[self.assignment.id],
            ),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assignment.refresh_from_db()
        self.assertTrue(self.assignment.is_primary)
        self.assertEqual(
            self.assignment.role,
            TeacherGroupSubject.RoleChoices.PRIMARY,
        )
