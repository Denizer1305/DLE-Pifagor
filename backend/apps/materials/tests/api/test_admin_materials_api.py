from __future__ import annotations

from apps.materials.models import Material, MaterialUsageLog
from apps.materials.tests.factories import create_material as factory_create_material
from apps.materials.tests.factories import (
    create_material_category,
    create_superadmin,
    extract_results,
    unique_slug,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AdminMaterialsApiTestCase(APITestCase):
    """
    API-тесты административного управления материалами.
    """

    def setUp(self) -> None:
        """
        Подготавливает тестовые данные.
        """

        self.superadmin = create_superadmin(
            email="materials-admin@example.com",
        )
        self.category = create_material_category(
            name="Материалы администратора",
            slug=unique_slug("admin-materials-category"),
        )
        self.material = factory_create_material(
            title="Основы алгоритмизации",
            slug=unique_slug("admin-algorithms"),
            category=self.category,
            material_type=Material.MaterialTypeChoices.TEXT,
            status=Material.StatusChoices.DRAFT,
            visibility=Material.VisibilityChoices.PRIVATE,
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

    def test_superadmin_can_get_material_detail(self) -> None:
        """
        Суперадмин получает карточку материала.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse(
                "materials_admin:materials-admin-materials-detail",
                kwargs={"pk": self.material.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], self.material.id)
        self.assertEqual(response.json()["title"], self.material.title)

    def test_superadmin_can_create_material(self) -> None:
        """
        Суперадмин создаёт материал.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("materials_admin:materials-admin-materials-list"),
            {
                "title": "Конспект по Pascal",
                "slug": unique_slug("admin-pascal-notes"),
                "short_description": "Краткий конспект.",
                "description": "Материал для занятия по Pascal.",
                "material_type": Material.MaterialTypeChoices.TEXT,
                "status": Material.StatusChoices.DRAFT,
                "visibility": Material.VisibilityChoices.PRIVATE,
                "source": Material.SourceChoices.MANUAL,
                "category_id": self.category.id,
                "tags": [
                    "pascal",
                    "конспект",
                ],
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], "Конспект по Pascal")
        self.assertEqual(
            response.json()["material_type"],
            Material.MaterialTypeChoices.TEXT,
        )

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
                "short_description": "Обновлённое описание.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.material.refresh_from_db()

        self.assertEqual(
            self.material.title,
            "Основы алгоритмизации и программирования",
        )
        self.assertEqual(
            self.material.short_description,
            "Обновлённое описание.",
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
        self.assertTrue(self.material.is_active)
        self.assertIsNotNone(self.material.published_at)
        self.assertTrue(
            MaterialUsageLog.objects.filter(
                material=self.material,
                action=MaterialUsageLog.ActionChoices.PUBLISH,
            ).exists()
        )

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
        self.assertIsNotNone(self.material.archived_at)
        self.assertTrue(
            MaterialUsageLog.objects.filter(
                material=self.material,
                action=MaterialUsageLog.ActionChoices.ARCHIVE,
            ).exists()
        )

    def test_superadmin_can_restore_material(self) -> None:
        """
        Суперадмин восстанавливает материал из архива.
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
        self.assertIsNone(self.material.archived_at)

    def test_superadmin_destroy_archives_material(self) -> None:
        """
        DELETE в админском API архивирует материал вместо физического удаления.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.delete(
            reverse(
                "materials_admin:materials-admin-materials-detail",
                kwargs={"pk": self.material.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.material.refresh_from_db()

        self.assertEqual(self.material.status, Material.StatusChoices.ARCHIVED)
        self.assertFalse(self.material.is_active)

    def test_superadmin_can_log_material_usage(self) -> None:
        """
        Суперадмин может залогировать использование материала.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "materials_admin:materials-admin-materials-log-usage",
                kwargs={"pk": self.material.id},
            ),
            {
                "action": MaterialUsageLog.ActionChoices.VIEW,
                "context": MaterialUsageLog.ContextChoices.ADMIN,
                "metadata": {
                    "source": "test",
                },
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json()["action"],
            MaterialUsageLog.ActionChoices.VIEW,
        )

        self.assertTrue(
            MaterialUsageLog.objects.filter(
                material=self.material,
                action=MaterialUsageLog.ActionChoices.VIEW,
            ).exists()
        )

    def test_filter_materials_by_search(self) -> None:
        """
        Фильтр search ищет материал по названию.
        """

        another_material = factory_create_material(
            title="Рабочая тетрадь",
            slug=unique_slug("admin-workbook"),
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
