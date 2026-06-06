from __future__ import annotations

from apps.organizations.constants import StudyGroupStatus
from apps.organizations.tests.factories import (
    create_department,
    create_organization,
    create_study_group,
    create_superadmin,
    create_test_user,
)
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class AdminStudyGroupsApiTestCase(TestCase):
    """
    Тесты административного API учебных групп.
    """

    def setUp(self) -> None:
        self.client = APIClient()

        self.superadmin = create_superadmin(
            email="superadmin@example.com",
            phone="+79993000001",
        )
        self.regular_user = create_test_user(
            email="regular@example.com",
            phone="+79993000002",
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
        self.group = create_study_group(
            organization=self.organization,
            department=self.department,
            name="ИС-21",
            code="is_21",
        )

    def test_regular_user_cannot_get_groups_list(self) -> None:
        """
        Обычный пользователь не может получить список групп админки.
        """

        self.client.force_authenticate(user=self.regular_user)

        url = reverse("organizations:admin-study-groups-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superadmin_can_get_groups_list(self) -> None:
        """
        Суперадмин может получить список групп.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-study-groups-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        group_ids = {item["id"] for item in payload}

        self.assertIn(self.group.id, group_ids)

    def test_superadmin_can_get_group_detail(self) -> None:
        """
        Суперадмин может получить детальную карточку группы.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-study-groups-detail",
            kwargs={"pk": self.group.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["id"], self.group.id)
        self.assertEqual(payload["code"], "is_21")

    def test_superadmin_can_create_group(self) -> None:
        """
        Суперадмин может создать учебную группу.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-study-groups-list")
        response = self.client.post(
            url,
            {
                "organization_id": self.organization.id,
                "department_id": self.department.id,
                "name": "ИС-22",
                "code": "is_22",
                "admission_year": 2024,
                "graduation_year": 2028,
                "course_number": 1,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payload = response.json()

        self.assertEqual(payload["name"], "ИС-22")
        self.assertEqual(payload["code"], "is_22")
        self.assertEqual(payload["organization"]["id"], self.organization.id)
        self.assertEqual(payload["department"]["id"], self.department.id)

    def test_superadmin_can_update_group(self) -> None:
        """
        Суперадмин может обновить учебную группу.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-study-groups-detail",
            kwargs={"pk": self.group.id},
        )
        response = self.client.patch(
            url,
            {
                "course_number": 3,
                "description": "Обновлённое описание группы.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["course_number"], 3)
        self.assertEqual(payload["description"], "Обновлённое описание группы.")

    def test_superadmin_can_archive_group(self) -> None:
        """
        DELETE архивирует группу.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-study-groups-detail",
            kwargs={"pk": self.group.id},
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.group.refresh_from_db()

        self.assertEqual(self.group.status, StudyGroupStatus.ARCHIVED)
        self.assertFalse(self.group.is_active)
        self.assertTrue(self.group.is_archived)

    def test_superadmin_can_restore_group(self) -> None:
        """
        Суперадмин может восстановить группу из архива.
        """

        self.group.status = StudyGroupStatus.ARCHIVED
        self.group.save(update_fields=["status", "is_active", "is_archived"])

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-study-groups-restore",
            kwargs={"pk": self.group.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.group.refresh_from_db()

        self.assertEqual(self.group.status, StudyGroupStatus.ACTIVE)
        self.assertTrue(self.group.is_active)
        self.assertFalse(self.group.is_archived)

    def test_superadmin_can_set_group_join_code(self) -> None:
        """
        Суперадмин может установить код вступления в группу.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-study-groups-set-join-code",
            kwargs={"pk": self.group.id},
        )
        response = self.client.post(
            url,
            {
                "raw_code": "group-code-123",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["raw_code"], "group-code-123")

        self.group.refresh_from_db()

        self.assertTrue(self.group.has_active_join_code)

    def test_superadmin_can_disable_group_join_code(self) -> None:
        """
        Суперадмин может отключить код вступления в группу.
        """

        self.group.set_join_code(
            "group-code-123",
            save=True,
        )

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-study-groups-disable-join-code",
            kwargs={"pk": self.group.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.group.refresh_from_db()

        self.assertFalse(self.group.join_code_is_active)

    def test_superadmin_can_clear_group_join_code(self) -> None:
        """
        Суперадмин может очистить код вступления в группу.
        """

        self.group.set_join_code(
            "group-code-123",
            save=True,
        )

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-study-groups-clear-join-code",
            kwargs={"pk": self.group.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.group.refresh_from_db()

        self.assertEqual(self.group.join_code_hash, "")
        self.assertFalse(self.group.join_code_is_active)
        self.assertIsNone(self.group.join_code_expires_at)