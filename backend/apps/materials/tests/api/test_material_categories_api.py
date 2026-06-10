from __future__ import annotations

from apps.materials.tests.factories import (
    create_material_category,
    create_superadmin,
    extract_results,
    unique_slug,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class MaterialCategoryApiTestCase(APITestCase):
    """
    API-тесты категорий учебных материалов.
    """

    def setUp(self) -> None:
        """
        Подготавливает тестовые данные.
        """

        self.superadmin = create_superadmin()
        self.category = create_material_category(
            name="Презентации",
            slug=unique_slug("presentations"),
        )

    def test_superadmin_can_get_categories_list(self) -> None:
        """
        Суперадмин получает список категорий.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("materials_admin:materials-admin-categories-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        category_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.category.id, category_ids)

    def test_superadmin_can_create_category(self) -> None:
        """
        Суперадмин создаёт категорию.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("materials_admin:materials-admin-categories-list"),
            {
                "name": "Методички",
                "slug": unique_slug("methods"),
                "description": "Методические материалы.",
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_superadmin_can_deactivate_category(self) -> None:
        """
        Суперадмин деактивирует категорию.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "materials_admin:materials-admin-categories-deactivate",
                kwargs={"pk": self.category.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.category.refresh_from_db()

        self.assertFalse(self.category.is_active)

    def test_superadmin_can_restore_category(self) -> None:
        """
        Суперадмин восстанавливает категорию.
        """

        self.category.is_active = False
        self.category.save(update_fields=["is_active"])

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "materials_admin:materials-admin-categories-restore",
                kwargs={"pk": self.category.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.category.refresh_from_db()

        self.assertTrue(self.category.is_active)

    def test_filter_categories_by_search(self) -> None:
        """
        Фильтр search ищет категорию по названию.
        """

        another_category = create_material_category(
            name="Лабораторные работы",
            slug=unique_slug("labs"),
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(
            reverse("materials_admin:materials-admin-categories-list"),
            {
                "search": "През",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        category_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.category.id, category_ids)
        self.assertNotIn(another_category.id, category_ids)
