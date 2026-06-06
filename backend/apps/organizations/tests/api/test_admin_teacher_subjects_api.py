from __future__ import annotations

from apps.organizations.models import TeacherSubject
from apps.organizations.tests.factories import (
    create_organization,
    create_subject,
    create_superadmin,
    create_teacher,
    create_teacher_subject,
    create_test_user,
)
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class AdminTeacherSubjectsApiTestCase(TestCase):
    """
    Тесты административного API предметов преподавателей.
    """

    def setUp(self) -> None:
        self.client = APIClient()

        self.superadmin = create_superadmin(
            email="superadmin-teacher-subjects-api@example.com",
            phone="+79998100001",
        )
        self.regular_user = create_test_user(
            email="regular-teacher-subjects-api@example.com",
            phone="+79998100002",
        )

        self.organization = create_organization(
            name="Организация предметов преподавателей",
            short_name="Предметы",
            code="teacher_subjects_org",
            slug="teacher-subjects-org",
        )

        self.teacher = create_teacher(
            organization=self.organization,
            email="teacher-subject-api@example.com",
            phone="+79998100003",
            first_name="Иван",
            last_name="Иванов",
            position="Преподаватель",
        )
        self.second_teacher = create_teacher(
            organization=self.organization,
            email="second-teacher-subject-api@example.com",
            phone="+79998100004",
            first_name="Пётр",
            last_name="Петров",
            position="Преподаватель",
        )

        self.math = create_subject(
            name="Математика",
            short_name="Математика",
            code="math",
            is_active=True,
        )
        self.physics = create_subject(
            name="Физика",
            short_name="Физика",
            code="physics",
            is_active=True,
        )
        self.history = create_subject(
            name="История",
            short_name="История",
            code="history",
            is_active=True,
        )

        self.teacher_subject = create_teacher_subject(
            teacher=self.teacher,
            subject=self.math,
            is_primary=True,
            is_active=True,
        )

    def test_regular_user_cannot_get_teacher_subjects_list(self) -> None:
        """
        Обычный пользователь не может получить список предметов преподавателей.
        """

        self.client.force_authenticate(user=self.regular_user)

        url = reverse("organizations:admin-teacher-subjects-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superadmin_can_get_teacher_subjects_list(self) -> None:
        """
        Суперадмин может получить список предметов преподавателей.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-teacher-subjects-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        relation_ids = {item["id"] for item in payload}

        self.assertIn(self.teacher_subject.id, relation_ids)

    def test_superadmin_can_get_teacher_subject_detail(self) -> None:
        """
        Суперадмин может получить детальную карточку предмета преподавателя.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-teacher-subjects-detail",
            kwargs={"pk": self.teacher_subject.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["id"], self.teacher_subject.id)
        self.assertEqual(payload["teacher"], self.teacher.id)
        self.assertEqual(payload["subject"]["id"], self.math.id)

    def test_superadmin_can_create_teacher_subject(self) -> None:
        """
        Суперадмин может назначить предмет преподавателю.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-teacher-subjects-list")
        response = self.client.post(
            url,
            {
                "teacher_id": self.second_teacher.id,
                "subject_id": self.physics.id,
                "is_primary": True,
                "is_active": True,
                "notes": "Назначено через API.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payload = response.json()

        self.assertEqual(payload["teacher"], self.second_teacher.id)
        self.assertEqual(payload["subject"]["id"], self.physics.id)
        self.assertTrue(payload["is_primary"])
        self.assertEqual(payload["notes"], "Назначено через API.")

    def test_superadmin_can_update_teacher_subject(self) -> None:
        """
        Суперадмин может обновить предмет преподавателя.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-teacher-subjects-detail",
            kwargs={"pk": self.teacher_subject.id},
        )
        response = self.client.patch(
            url,
            {
                "subject_id": self.physics.id,
                "is_primary": False,
                "notes": "Обновлено через API.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["subject"]["id"], self.physics.id)
        self.assertFalse(payload["is_primary"])
        self.assertEqual(payload["notes"], "Обновлено через API.")

    def test_superadmin_can_deactivate_teacher_subject(self) -> None:
        """
        DELETE деактивирует предмет преподавателя.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-teacher-subjects-detail",
            kwargs={"pk": self.teacher_subject.id},
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.teacher_subject.refresh_from_db()

        self.assertFalse(self.teacher_subject.is_active)
        self.assertFalse(self.teacher_subject.is_primary)

    def test_superadmin_can_restore_teacher_subject(self) -> None:
        """
        Суперадмин может восстановить предмет преподавателя.
        """

        self.teacher_subject.is_active = False
        self.teacher_subject.is_primary = False
        self.teacher_subject.save(
            update_fields=[
                "is_active",
                "is_primary",
            ]
        )

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-teacher-subjects-restore",
            kwargs={"pk": self.teacher_subject.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.teacher_subject.refresh_from_db()

        self.assertTrue(self.teacher_subject.is_active)

    def test_superadmin_can_set_primary_teacher_subject(self) -> None:
        """
        Суперадмин может сделать предмет основным для преподавателя.
        """

        second_subject = create_teacher_subject(
            teacher=self.teacher,
            subject=self.physics,
            is_primary=False,
            is_active=True,
        )

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-teacher-subjects-set-primary",
            kwargs={"pk": second_subject.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.teacher_subject.refresh_from_db()
        second_subject.refresh_from_db()

        self.assertFalse(self.teacher_subject.is_primary)
        self.assertTrue(second_subject.is_primary)

    def test_cannot_assign_subject_to_regular_user(self) -> None:
        """
        Нельзя назначить предмет пользователю без роли преподавателя.
        """

        user_without_teacher_role = create_test_user(
            email="not-teacher-subject-api@example.com",
            phone="+79998100005",
        )

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-teacher-subjects-list")
        response = self.client.post(
            url,
            {
                "teacher_id": user_without_teacher_role.id,
                "subject_id": self.history.id,
                "is_primary": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertFalse(
            TeacherSubject.objects.filter(
                teacher=user_without_teacher_role,
                subject=self.history,
            ).exists()
        )

    def test_cannot_assign_inactive_subject_to_teacher(self) -> None:
        """
        Нельзя назначить преподавателю неактивный предмет.
        """

        inactive_subject = create_subject(
            name="Неактивный предмет",
            short_name="Неактивный",
            code="inactive_subject_api",
            is_active=False,
        )

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-teacher-subjects-list")
        response = self.client.post(
            url,
            {
                "teacher_id": self.second_teacher.id,
                "subject_id": inactive_subject.id,
                "is_primary": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertFalse(
            TeacherSubject.objects.filter(
                teacher=self.second_teacher,
                subject=inactive_subject,
            ).exists()
        )

    def test_filter_teacher_subjects_by_subject_id(self) -> None:
        """
        Фильтр subject_id возвращает связи с указанным предметом.
        """

        physics_relation = create_teacher_subject(
            teacher=self.second_teacher,
            subject=self.physics,
            is_primary=True,
            is_active=True,
        )

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-teacher-subjects-list")
        response = self.client.get(
            url,
            {
                "subject_id": self.physics.id,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        relation_ids = {item["id"] for item in payload}

        self.assertIn(physics_relation.id, relation_ids)
        self.assertNotIn(self.teacher_subject.id, relation_ids)