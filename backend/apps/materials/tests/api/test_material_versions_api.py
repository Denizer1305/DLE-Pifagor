from __future__ import annotations

from apps.materials.models import Material, MaterialVersion
from apps.materials.tests.factories import (
    create_material,
    create_material_version,
    create_superadmin,
    extract_results,
    unique_slug,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class MaterialVersionApiTestCase(APITestCase):
    """
    API-тесты версий учебных материалов.
    """

    def setUp(self) -> None:
        """
        Подготавливает тестовые данные.
        """

        self.superadmin = create_superadmin()
        self.material = create_material(
            title="Текстовый материал",
            slug=unique_slug("text-material"),
            material_type=Material.MaterialTypeChoices.TEXT,
        )
        self.version = create_material_version(
            material=self.material,
            version_number=1,
            status=MaterialVersion.StatusChoices.DRAFT,
            content="Первая версия материала.",
        )

    def test_superadmin_can_get_versions_list(self) -> None:
        """
        Суперадмин получает список версий.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("materials_admin:materials-admin-versions-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        version_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.version.id, version_ids)

    def test_superadmin_can_create_version(self) -> None:
        """
        Суперадмин создаёт версию материала.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("materials_admin:materials-admin-versions-list"),
            {
                "material_id": self.material.id,
                "version_number": 2,
                "status": MaterialVersion.StatusChoices.DRAFT,
                "content": "Вторая версия материала.",
                "change_log": "Добавлен новый текст.",
                "is_current": False,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["version_number"], 2)

    def test_superadmin_can_set_current_version(self) -> None:
        """
        Суперадмин делает версию текущей.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "materials_admin:materials-admin-versions-set-current",
                kwargs={"pk": self.version.id},
            ),
            {
                "confirm": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.version.refresh_from_db()
        self.material.refresh_from_db()

        self.assertTrue(self.version.is_current)
        self.assertEqual(self.material.current_version_id, self.version.id)

    def test_superadmin_can_archive_version(self) -> None:
        """
        Суперадмин архивирует версию материала.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "materials_admin:materials-admin-versions-archive",
                kwargs={"pk": self.version.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.version.refresh_from_db()

        self.assertEqual(
            self.version.status,
            MaterialVersion.StatusChoices.ARCHIVED,
        )
        self.assertFalse(self.version.is_current)

    def test_filter_versions_by_material(self) -> None:
        """
        Фильтр material_id ограничивает версии материалом.
        """

        another_material = create_material(
            title="Другой материал",
            slug=unique_slug("another-material"),
            material_type=Material.MaterialTypeChoices.TEXT,
        )
        another_version = create_material_version(
            material=another_material,
            version_number=1,
            content="Версия другого материала.",
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("materials_admin:materials-admin-versions-list"),
            {
                "material_id": self.material.id,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        version_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.version.id, version_ids)
        self.assertNotIn(another_version.id, version_ids)
