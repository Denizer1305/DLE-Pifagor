from __future__ import annotations

from apps.organizations.models import GroupCurator
from apps.organizations.tests.factories import (
    create_department,
    create_group_curator,
    create_organization,
    create_study_group,
    create_superadmin,
    create_teacher,
    create_test_user,
)
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class AdminGroupCuratorsApiTestCase(TestCase):
    """
    Тесты административного API кураторов групп.
    """

    def setUp(self) -> None:
        self.client = APIClient()

        self.superadmin = create_superadmin(
            email="superadmin@example.com",
            phone="+79995000001",
        )
        self.regular_user = create_test_user(
            email="regular@example.com",
            phone="+79995000002",
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
        self.second_group = create_study_group(
            organization=self.organization,
            department=self.department,
            name="ИС-22",
            code="is_22",
        )

        self.teacher = create_teacher(
            organization=self.organization,
            email="teacher@example.com",
            phone="+79995000003",
            first_name="Иван",
            last_name="Иванов",
            position="Преподаватель",
        )
        self.second_teacher = create_teacher(
            organization=self.organization,
            email="second-teacher@example.com",
            phone="+79995000004",
            first_name="Пётр",
            last_name="Петров",
            position="Преподаватель",
        )

        self.group_curator = create_group_curator(
            group=self.group,
            teacher=self.teacher,
            is_primary=True,
            is_active=True,
        )

    def test_regular_user_cannot_get_group_curators_list(self) -> None:
        """
        Обычный пользователь не может получить список кураторов групп.
        """

        self.client.force_authenticate(user=self.regular_user)

        url = reverse("organizations:admin-group-curators-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superadmin_can_get_group_curators_list(self) -> None:
        """
        Суперадмин может получить список кураторов групп.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-group-curators-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        curator_ids = {item["id"] for item in payload}

        self.assertIn(self.group_curator.id, curator_ids)

    def test_superadmin_can_get_group_curator_detail(self) -> None:
        """
        Суперадмин может получить детальную карточку куратора группы.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-group-curators-detail",
            kwargs={"pk": self.group_curator.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["id"], self.group_curator.id)
        self.assertEqual(payload["group"]["id"], self.group.id)
        self.assertEqual(payload["teacher"], self.teacher.id)

    def test_superadmin_can_create_group_curator(self) -> None:
        """
        Суперадмин может назначить куратора группе.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-group-curators-list")
        response = self.client.post(
            url,
            {
                "group_id": self.second_group.id,
                "teacher_id": self.second_teacher.id,
                "is_primary": True,
                "is_active": True,
                "notes": "Назначен через API.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payload = response.json()

        self.assertEqual(payload["group"]["id"], self.second_group.id)
        self.assertEqual(payload["teacher"], self.second_teacher.id)
        self.assertTrue(payload["is_primary"])
        self.assertEqual(payload["notes"], "Назначен через API.")

    def test_superadmin_can_update_group_curator(self) -> None:
        """
        Суперадмин может обновить куратора группы.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-group-curators-detail",
            kwargs={"pk": self.group_curator.id},
        )
        response = self.client.patch(
            url,
            {
                "notes": "Обновлено через API.",
                "is_primary": False,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["notes"], "Обновлено через API.")
        self.assertFalse(payload["is_primary"])

    def test_superadmin_can_remove_group_curator(self) -> None:
        """
        DELETE деактивирует куратора группы.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-group-curators-detail",
            kwargs={"pk": self.group_curator.id},
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.group_curator.refresh_from_db()

        self.assertFalse(self.group_curator.is_active)
        self.assertFalse(self.group_curator.is_primary)

    def test_superadmin_can_set_primary_group_curator(self) -> None:
        """
        Суперадмин может сделать куратора основным для группы.
        """

        second_curator = create_group_curator(
            group=self.group,
            teacher=self.second_teacher,
            is_primary=False,
            is_active=True,
        )

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-group-curators-set-primary",
            kwargs={"pk": second_curator.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.group_curator.refresh_from_db()
        second_curator.refresh_from_db()

        self.assertFalse(self.group_curator.is_primary)
        self.assertTrue(second_curator.is_primary)

    def test_cannot_assign_regular_user_as_group_curator(self) -> None:
        """
        Нельзя назначить куратором пользователя без роли преподавателя.
        """

        user_without_teacher_role = create_test_user(
            email="not-teacher@example.com",
            phone="+79995000005",
        )

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-group-curators-list")
        response = self.client.post(
            url,
            {
                "group_id": self.second_group.id,
                "teacher_id": user_without_teacher_role.id,
                "is_primary": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertFalse(
            GroupCurator.objects.filter(
                group=self.second_group,
                teacher=user_without_teacher_role,
            ).exists()
        )
