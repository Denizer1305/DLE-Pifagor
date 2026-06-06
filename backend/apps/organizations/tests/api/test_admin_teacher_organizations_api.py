from __future__ import annotations

from apps.organizations.constants import TeacherEmploymentType
from apps.organizations.models import TeacherOrganization
from apps.organizations.tests.factories import (
    create_organization,
    create_superadmin,
    create_teacher,
    create_teacher_organization,
    create_test_user,
)
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class AdminTeacherOrganizationsApiTestCase(TestCase):
    """
    Тесты административного API связей преподавателей с организациями.
    """

    def setUp(self) -> None:
        self.client = APIClient()

        self.superadmin = create_superadmin(
            email="superadmin@example.com",
            phone="+79994000001",
        )
        self.regular_user = create_test_user(
            email="regular@example.com",
            phone="+79994000002",
        )

        self.organization = create_organization(
            name="ГАПОУ ВО «ВлГК им. Д.К. Советкина»",
            short_name="ВлГК",
            code="vlgk",
            slug="vlgk",
        )
        self.second_organization = create_organization(
            name="Вторая образовательная организация",
            short_name="Вторая ОО",
            code="second_org",
            slug="second-org",
        )

        self.teacher = create_teacher(
            organization=self.organization,
            email="teacher@example.com",
            phone="+79994000003",
            first_name="Иван",
            last_name="Иванов",
            position="Преподаватель",
        )

        self.teacher_organization = create_teacher_organization(
            teacher=self.teacher,
            organization=self.organization,
            position="Преподаватель математики",
            employment_type=TeacherEmploymentType.FULL_TIME,
            is_primary=True,
            is_active=True,
        )

    def test_regular_user_cannot_get_teacher_organizations_list(self) -> None:
        """
        Обычный пользователь не может получить список связей преподавателей.
        """

        self.client.force_authenticate(user=self.regular_user)

        url = reverse("organizations:admin-teacher-organizations-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superadmin_can_get_teacher_organizations_list(self) -> None:
        """
        Суперадмин может получить список связей преподавателей с организациями.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-teacher-organizations-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        relation_ids = {item["id"] for item in payload}

        self.assertIn(self.teacher_organization.id, relation_ids)

    def test_superadmin_can_get_teacher_organization_detail(self) -> None:
        """
        Суперадмин может получить детальную карточку связи.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-teacher-organizations-detail",
            kwargs={"pk": self.teacher_organization.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["id"], self.teacher_organization.id)
        self.assertEqual(payload["position"], "Преподаватель математики")
        self.assertEqual(payload["organization"]["id"], self.organization.id)

    def test_superadmin_can_create_teacher_organization(self) -> None:
        """
        Суперадмин может привязать преподавателя к организации.
        """

        self.teacher_organization.delete()

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-teacher-organizations-list")
        response = self.client.post(
            url,
            {
                "teacher_id": self.teacher.id,
                "organization_id": self.organization.id,
                "position": "Преподаватель информатики",
                "employment_type": TeacherEmploymentType.FULL_TIME,
                "is_primary": True,
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payload = response.json()

        self.assertEqual(payload["teacher"], self.teacher.id)
        self.assertEqual(payload["organization"]["id"], self.organization.id)
        self.assertEqual(payload["position"], "Преподаватель информатики")
        self.assertTrue(payload["is_primary"])

    def test_superadmin_can_update_teacher_organization(self) -> None:
        """
        Суперадмин может обновить связь преподавателя с организацией.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-teacher-organizations-detail",
            kwargs={"pk": self.teacher_organization.id},
        )
        response = self.client.patch(
            url,
            {
                "position": "Старший преподаватель",
                "employment_type": TeacherEmploymentType.PART_TIME,
                "notes": "Обновлено через API.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["position"], "Старший преподаватель")
        self.assertEqual(payload["employment_type"], TeacherEmploymentType.PART_TIME)
        self.assertEqual(payload["notes"], "Обновлено через API.")

    def test_superadmin_can_detach_teacher_from_organization(self) -> None:
        """
        DELETE деактивирует связь преподавателя с организацией.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-teacher-organizations-detail",
            kwargs={"pk": self.teacher_organization.id},
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.teacher_organization.refresh_from_db()

        self.assertFalse(self.teacher_organization.is_active)
        self.assertFalse(self.teacher_organization.is_primary)

    def test_superadmin_can_set_primary_teacher_organization(self) -> None:
        """
        Суперадмин может сделать организацию основной для преподавателя.
        """

        second_relation = create_teacher_organization(
            teacher=self.teacher,
            organization=self.second_organization,
            position="Преподаватель",
            employment_type=TeacherEmploymentType.PART_TIME,
            is_primary=False,
            is_active=True,
        )

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-teacher-organizations-set-primary",
            kwargs={"pk": second_relation.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.teacher_organization.refresh_from_db()
        second_relation.refresh_from_db()

        self.assertFalse(self.teacher_organization.is_primary)
        self.assertTrue(second_relation.is_primary)

    def test_cannot_attach_regular_user_as_teacher(self) -> None:
        """
        Нельзя привязать пользователя без роли преподавателя как преподавателя.
        """

        user_without_teacher_role = create_test_user(
            email="not-teacher@example.com",
            phone="+79994000004",
        )

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-teacher-organizations-list")
        response = self.client.post(
            url,
            {
                "teacher_id": user_without_teacher_role.id,
                "organization_id": self.organization.id,
                "position": "Не преподаватель",
                "employment_type": TeacherEmploymentType.FULL_TIME,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertFalse(
            TeacherOrganization.objects.filter(
                teacher=user_without_teacher_role,
                organization=self.organization,
            ).exists()
        )