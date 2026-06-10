from __future__ import annotations

from apps.organizations.tests.factories import (
    create_organization,
    create_superadmin,
    create_test_user,
)
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class AdminOrganizationsApiTestCase(TestCase):
    """
    Тесты административного API организаций.
    """

    def setUp(self) -> None:
        self.client = APIClient()

        self.superadmin = create_superadmin(
            email="superadmin@example.com",
            phone="+79991000001",
        )
        self.regular_user = create_test_user(
            email="regular@example.com",
            phone="+79991000002",
        )

        self.organization = create_organization(
            name="ГАПОУ ВО «ВлГК им. Д.К. Советкина»",
            short_name="ВлГК",
            code="vlgk",
            slug="vlgk",
            is_public=True,
            is_default_public=True,
        )

    def test_regular_user_cannot_get_organizations_list(self) -> None:
        """
        Обычный пользователь не может получить список организаций админки.
        """

        self.client.force_authenticate(user=self.regular_user)

        url = reverse("organizations:admin-organizations-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superadmin_can_get_organizations_list(self) -> None:
        """
        Суперадмин может получить список организаций.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-organizations-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        organization_ids = {item["id"] for item in payload}

        self.assertIn(self.organization.id, organization_ids)

    def test_superadmin_can_get_organization_detail(self) -> None:
        """
        Суперадмин может получить детальную карточку организации.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-organizations-detail",
            kwargs={"pk": self.organization.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["id"], self.organization.id)
        self.assertEqual(payload["code"], "vlgk")

    def test_superadmin_can_create_organization(self) -> None:
        """
        Суперадмин может создать организацию.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-organizations-list")
        response = self.client.post(
            url,
            {
                "name": "Новая образовательная организация",
                "short_name": "Новая ОО",
                "code": "new_org",
                "slug": "new-org",
                "city": "Владимир",
                "is_public": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payload = response.json()

        self.assertEqual(payload["name"], "Новая образовательная организация")
        self.assertEqual(payload["code"], "new_org")

    def test_superadmin_can_update_organization(self) -> None:
        """
        Суперадмин может обновить организацию.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-organizations-detail",
            kwargs={"pk": self.organization.id},
        )
        response = self.client.patch(
            url,
            {
                "city": "Суздаль",
                "is_public": False,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["city"], "Суздаль")
        self.assertFalse(payload["is_public"])

    def test_superadmin_can_deactivate_organization(self) -> None:
        """
        DELETE деактивирует организацию, а не удаляет физически.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-organizations-detail",
            kwargs={"pk": self.organization.id},
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.organization.refresh_from_db()

        self.assertFalse(self.organization.is_active)

    def test_superadmin_can_restore_organization(self) -> None:
        """
        Суперадмин может восстановить организацию.
        """

        self.organization.is_active = False
        self.organization.save(update_fields=["is_active"])

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-organizations-restore",
            kwargs={"pk": self.organization.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.organization.refresh_from_db()

        self.assertTrue(self.organization.is_active)

    def test_superadmin_can_set_teacher_registration_code(self) -> None:
        """
        Суперадмин может установить код регистрации преподавателя.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-organizations-set-teacher-code",
            kwargs={"pk": self.organization.id},
        )
        response = self.client.post(
            url,
            {
                "raw_code": "teacher-code-123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["raw_code"], "teacher-code-123")

        self.organization.refresh_from_db()

        self.assertTrue(self.organization.has_active_teacher_registration_code)

    def test_superadmin_can_disable_teacher_registration_code(self) -> None:
        """
        Суперадмин может отключить код регистрации преподавателя.
        """

        self.organization.set_teacher_registration_code(
            "teacher-code-123",
            save=True,
        )

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-organizations-disable-teacher-code",
            kwargs={"pk": self.organization.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.organization.refresh_from_db()

        self.assertFalse(self.organization.teacher_registration_code_is_active)

    def test_superadmin_can_clear_teacher_registration_code(self) -> None:
        """
        Суперадмин может очистить код регистрации преподавателя.
        """

        self.organization.set_teacher_registration_code(
            "teacher-code-123",
            save=True,
        )

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-organizations-clear-teacher-code",
            kwargs={"pk": self.organization.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.organization.refresh_from_db()

        self.assertEqual(self.organization.teacher_registration_code_hash, "")
        self.assertFalse(self.organization.teacher_registration_code_is_active)
        self.assertIsNone(self.organization.teacher_registration_code_expires_at)
