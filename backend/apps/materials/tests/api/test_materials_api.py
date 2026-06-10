from __future__ import annotations

from apps.materials.models import Material
from apps.materials.tests.factories import (
    create_material,
    create_material_category,
    create_superadmin,
    extract_results,
    unique_slug,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class MaterialApiTestCase(APITestCase):
    """
    API-тесты учебных материалов.
    """

    def setUp(self) -> None:
        """
        Подготавливает тестовые данные.
        """

        self.superadmin = create_superadmin()
        self.category = create_material_category(
            name="Конспекты",
            slug=unique_slug("notes-category"),
        )
        self.material = create_material(
            title="Основы алгоритмизации",
            slug=unique_slug("algorithms"),
            category=self.category,
            material_type=Material.MaterialTypeChoices.TEXT,
            status=Material.StatusChoices.DRAFT,
        )

    def test_superadmin_can_get_materials_list(self) -> None:
        """
        Суперадмин получает список материалов.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("materials_admin:materials-admin-materials-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        material_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.material.id, material_ids)

    def test_superadmin_can_create_material(self) -> None:
        """
        Суперадмин создаёт материал.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("materials_admin:materials-admin-materials-list"),
            {
                "title": "Презентация по Pascal",
                "slug": unique_slug("pascal-presentation"),
                "short_description": "Вводная презентация.",
                "description": "Материал для первого занятия.",
                "material_type": Material.MaterialTypeChoices.TEXT,
                "status": Material.StatusChoices.DRAFT,
                "visibility": Material.VisibilityChoices.PRIVATE,
                "source": Material.SourceChoices.MANUAL,
                "category_id": self.category.id,
                "tags": [
                    "pascal",
                    "презентация",
                ],
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], "Презентация по Pascal")

    def test_superadmin_can_update_material(self) -> None:
        """
        Суперадмин обновляет материал.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.patch(
            reverse(
                "materials_admin:materials-admin-materials-detail",
                kwargs={"pk": self.material.id},
            ),
            {
                "title": "Основы алгоритмизации и программирования",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.material.refresh_from_db()

        self.assertEqual(
            self.material.title,
            "Основы алгоритмизации и программирования",
        )

    def test_superadmin_can_publish_material(self) -> None:
        """
        Суперадмин публикует материал.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "materials_admin:materials-admin-materials-publish",
                kwargs={"pk": self.material.id},
            ),
            {
                "confirm": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.material.refresh_from_db()

        self.assertEqual(self.material.status, Material.StatusChoices.PUBLISHED)
        self.assertIsNotNone(self.material.published_at)

    def test_superadmin_can_archive_material(self) -> None:
        """
        Суперадмин архивирует материал.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "materials_admin:materials-admin-materials-archive",
                kwargs={"pk": self.material.id},
            ),
            {
                "confirm": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.material.refresh_from_db()

        self.assertEqual(self.material.status, Material.StatusChoices.ARCHIVED)
        self.assertFalse(self.material.is_active)

    def test_superadmin_can_restore_material(self) -> None:
        """
        Суперадмин восстанавливает материал.
        """

        self.material.status = Material.StatusChoices.ARCHIVED
        self.material.is_active = False
        self.material.save(
            update_fields=[
                "status",
                "is_active",
            ]
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "materials_admin:materials-admin-materials-restore",
                kwargs={"pk": self.material.id},
            ),
            {
                "confirm": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.material.refresh_from_db()

        self.assertEqual(self.material.status, Material.StatusChoices.DRAFT)
        self.assertTrue(self.material.is_active)

    def test_filter_materials_by_search(self) -> None:
        """
        Фильтр search ищет материал по названию.
        """

        another_material = create_material(
            title="Рабочая тетрадь",
            slug=unique_slug("workbook"),
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("materials_admin:materials-admin-materials-list"),
            {
                "search": "алгоритм",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        material_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.material.id, material_ids)
        self.assertNotIn(another_material.id, material_ids)
