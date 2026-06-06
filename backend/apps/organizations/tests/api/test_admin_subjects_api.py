from __future__ import annotations

from apps.organizations.tests.factories import (
    create_subject,
    create_superadmin,
    create_test_user,
)
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class AdminSubjectsApiTestCase(TestCase):
    """
    Тесты административного API учебных предметов.
    """

    def setUp(self) -> None:
        self.client = APIClient()

        self.superadmin = create_superadmin(
            email="superadmin-subjects-api@example.com",
            phone="+79998000001",
        )
        self.regular_user = create_test_user(
            email="regular-subjects-api@example.com",
            phone="+79998000002",
        )

        self.subject = create_subject(
            name="Математика",
            short_name="Математика",
            code="math",
            is_active=True,
        )

    def test_regular_user_cannot_get_subjects_list(self) -> None:
        """
        Обычный пользователь не может получить список предметов админки.
        """

        self.client.force_authenticate(user=self.regular_user)

        url = reverse("organizations:admin-subjects-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superadmin_can_get_subjects_list(self) -> None:
        """
        Суперадмин может получить список учебных предметов.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-subjects-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        subject_ids = {item["id"] for item in payload}

        self.assertIn(self.subject.id, subject_ids)

    def test_superadmin_can_get_subject_detail(self) -> None:
        """
        Суперадмин может получить детальную карточку предмета.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-subjects-detail",
            kwargs={"pk": self.subject.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["id"], self.subject.id)
        self.assertEqual(payload["code"], "math")

    def test_superadmin_can_create_subject(self) -> None:
        """
        Суперадмин может создать учебный предмет.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-subjects-list")
        response = self.client.post(
            url,
            {
                "name": "Физика",
                "short_name": "Физика",
                "code": "physics",
                "description": "Учебный предмет.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        payload = response.json()

        self.assertEqual(payload["name"], "Физика")
        self.assertEqual(payload["code"], "physics")
        self.assertTrue(payload["is_active"])

    def test_superadmin_can_update_subject(self) -> None:
        """
        Суперадмин может обновить учебный предмет.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-subjects-detail",
            kwargs={"pk": self.subject.id},
        )
        response = self.client.patch(
            url,
            {
                "short_name": "Мат.",
                "description": "Обновлённое описание.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["short_name"], "Мат.")
        self.assertEqual(payload["description"], "Обновлённое описание.")

    def test_superadmin_can_deactivate_subject(self) -> None:
        """
        DELETE деактивирует предмет.
        """

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-subjects-detail",
            kwargs={"pk": self.subject.id},
        )
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.subject.refresh_from_db()

        self.assertFalse(self.subject.is_active)

    def test_superadmin_can_restore_subject(self) -> None:
        """
        Суперадмин может восстановить предмет.
        """

        self.subject.is_active = False
        self.subject.save(update_fields=["is_active"])

        self.client.force_authenticate(user=self.superadmin)

        url = reverse(
            "organizations:admin-subjects-restore",
            kwargs={"pk": self.subject.id},
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.subject.refresh_from_db()

        self.assertTrue(self.subject.is_active)

    def test_filter_subjects_by_search(self) -> None:
        """
        Фильтр search ищет предмет по названию, краткому названию или коду.
        """

        history = create_subject(
            name="История",
            short_name="История",
            code="history",
            is_active=True,
        )

        self.client.force_authenticate(user=self.superadmin)

        url = reverse("organizations:admin-subjects-list")
        response = self.client.get(
            url,
            {
                "search": "math",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        subject_ids = {item["id"] for item in payload}

        self.assertIn(self.subject.id, subject_ids)
        self.assertNotIn(history.id, subject_ids)