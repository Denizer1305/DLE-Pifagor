from __future__ import annotations

from apps.organizations.tests.factories import (
    create_department,
    create_organization,
    create_superadmin,
    create_test_user,
)
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class AdminDepartmentsApiTestCase(TestCase):
    """
    Тесты административного API отделений.
    """

    def setUp(self) -> None:
        self.client = APIClient()

        self.superadmin = create_superadmin(
            email="superadmin@example.com",
            phone="+79992000001",
        )
        self.regular_user = create_test_user(
            email="regular@example.com",
            phone="+79992000002",
        )

        self.organization = create_organization(
            name="ГАПОУ ВО «ВлГК им. Д.К. Советкина»",
            short_name="ВлГК",
            code="vlgk",
            slug="vlgk",
        )
        self.department = create_department(
            organization=self.organization,
            name="Отделение информационных технологий",
            short_name="ИТ",
            code="it",
        )

    def test_regular_user_cannot_get_departments_list(self) -> None:
        """
        Обычный пользователь не может получить список отделений админки.
        """

        self.client.force_authenticate(user=self.regular_user)

        url = reverse("organizations:admin-departments-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superadmin_can_get_departments_list(self) -> None:
        """
        Суперадмин может получить список отделений.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-departments-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        department_ids = {item["id"] for item in payload}

        self.assertIn(self.department.id, department_ids)

    def test_superadmin_can_get_department_detail(self) -> None:
        """
        Суперадмин может получить детальную карточку отделения.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-departments-detail",
            kwargs={"pk": self.department.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["id"], self.department.id)
        self.assertEqual(payload["code"], "it")

    def test_superadmin_can_create_department(self) -> None:
        """
        Суперадмин может создать отделение.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-departments-list")
        response = self.client.post(
            url,
            {
                "organization_id": self.organization.id,
                "name": "Экономическое отделение",
                "short_name": "Экономика",
                "code": "economics",
                "description": "Описание отделения.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payload = response.json()

        self.assertEqual(payload["name"], "Экономическое отделение")
        self.assertEqual(payload["code"], "economics")
        self.assertEqual(payload["organization"]["id"], self.organization.id)

    def test_superadmin_can_update_department(self) -> None:
        """
        Суперадмин может обновить отделение.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-departments-detail",
            kwargs={"pk": self.department.id},
        )
        response = self.client.patch(
            url,
            {
                "short_name": "ИТиПО",
                "description": "Обновлённое описание.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["short_name"], "ИТиПО")
        self.assertEqual(payload["description"], "Обновлённое описание.")

    def test_superadmin_can_deactivate_department(self) -> None:
        """
        DELETE деактивирует отделение.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-departments-detail",
            kwargs={"pk": self.department.id},
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.department.refresh_from_db()

        self.assertFalse(self.department.is_active)

    def test_superadmin_can_restore_department(self) -> None:
        """
        Суперадмин может восстановить отделение.
        """

        self.department.is_active = False
        self.department.save(update_fields=["is_active"])

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-departments-restore",
            kwargs={"pk": self.department.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.department.refresh_from_db()

        self.assertTrue(self.department.is_active)