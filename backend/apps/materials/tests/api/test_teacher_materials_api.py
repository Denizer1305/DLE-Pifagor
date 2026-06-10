from __future__ import annotations

from apps.materials.models import Material, MaterialUsageLog
from apps.materials.tests.factories import create_material as factory_create_material
from apps.materials.tests.factories import (
    create_material_category,
    create_user,
    extract_results,
    unique_slug,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TeacherMaterialsApiTestCase(APITestCase):
    """
    API-тесты материалов преподавателя.
    """

    def setUp(self) -> None:
        """
        Подготавливает тестовые данные.
        """

        self.teacher = create_user(
            email="materials-teacher@example.com",
            role_code="teacher",
        )
        self.other_teacher = create_user(
            email="materials-other-teacher@example.com",
            role_code="teacher",
        )
        self.regular_user = create_user(
            email="materials-regular-user@example.com",
        )

        self.category = create_material_category(
            name="Материалы преподавателя",
            slug=unique_slug("teacher-materials-category"),
        )
        self.own_material = factory_create_material(
            title="Материал преподавателя",
            slug=unique_slug("teacher-own-material"),
            owner=self.teacher,
            category=self.category,
            material_type=Material.MaterialTypeChoices.TEXT,
            visibility=Material.VisibilityChoices.PRIVATE,
            status=Material.StatusChoices.DRAFT,
        )
        self.foreign_material = factory_create_material(
            title="Чужой закрытый материал",
            slug=unique_slug("teacher-foreign-material"),
            owner=self.other_teacher,
            material_type=Material.MaterialTypeChoices.TEXT,
            visibility=Material.VisibilityChoices.PRIVATE,
            status=Material.StatusChoices.DRAFT,
        )
        self.public_material = factory_create_material(
            title="Публичный материал",
            slug=unique_slug("teacher-public-material"),
            material_type=Material.MaterialTypeChoices.TEXT,
            visibility=Material.VisibilityChoices.PUBLIC,
            status=Material.StatusChoices.PUBLISHED,
            is_active=True,
        )

    def test_teacher_can_get_available_materials_list(self) -> None:
        """
        Преподаватель видит свои материалы и публичные опубликованные материалы.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(
            reverse("materials_teacher:materials-teacher-materials-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        material_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.own_material.id, material_ids)
        self.assertIn(self.public_material.id, material_ids)
        self.assertNotIn(self.foreign_material.id, material_ids)

    def test_teacher_can_get_own_material_detail(self) -> None:
        """
        Преподаватель может получить карточку своего материала.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(
            reverse(
                "materials_teacher:materials-teacher-materials-detail",
                kwargs={"pk": self.own_material.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], self.own_material.id)

    def test_teacher_cannot_get_foreign_private_material_detail(self) -> None:
        """
        Преподаватель не получает чужой приватный материал.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.get(
            reverse(
                "materials_teacher:materials-teacher-materials-detail",
                kwargs={"pk": self.foreign_material.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_teacher_can_create_material(self) -> None:
        """
        Преподаватель создаёт материал через teacher API.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.post(
            reverse("materials_teacher:materials-teacher-materials-list"),
            {
                "title": "Новый материал преподавателя",
                "slug": unique_slug("teacher-created-material"),
                "short_description": "Материал для курса.",
                "description": "Описание материала.",
                "material_type": Material.MaterialTypeChoices.TEXT,
                "status": Material.StatusChoices.DRAFT,
                "visibility": Material.VisibilityChoices.PRIVATE,
                "source": Material.SourceChoices.MANUAL,
                "category_id": self.category.id,
                "tags": [
                    "курс",
                    "урок",
                ],
                "is_active": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json()["title"],
            "Новый материал преподавателя",
        )

        created_material = Material.objects.get(id=response.json()["id"])

        self.assertEqual(created_material.owner, self.teacher)

    def test_teacher_can_update_own_material(self) -> None:
        """
        Преподаватель обновляет свой материал.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.patch(
            reverse(
                "materials_teacher:materials-teacher-materials-detail",
                kwargs={"pk": self.own_material.id},
            ),
            {
                "title": "Обновлённый материал преподавателя",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.own_material.refresh_from_db()

        self.assertEqual(
            self.own_material.title,
            "Обновлённый материал преподавателя",
        )

    def test_teacher_cannot_update_foreign_private_material(self) -> None:
        """
        Преподаватель не может обновить чужой приватный материал.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.patch(
            reverse(
                "materials_teacher:materials-teacher-materials-detail",
                kwargs={"pk": self.foreign_material.id},
            ),
            {
                "title": "Попытка изменить чужой материал",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.foreign_material.refresh_from_db()

        self.assertEqual(
            self.foreign_material.title,
            "Чужой закрытый материал",
        )

    def test_teacher_can_publish_own_material(self) -> None:
        """
        Преподаватель публикует свой материал.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.post(
            reverse(
                "materials_teacher:materials-teacher-materials-publish",
                kwargs={"pk": self.own_material.id},
            ),
            {
                "confirm": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.own_material.refresh_from_db()

        self.assertEqual(
            self.own_material.status,
            Material.StatusChoices.PUBLISHED,
        )
        self.assertIsNotNone(self.own_material.published_at)

    def test_teacher_can_archive_own_material(self) -> None:
        """
        Преподаватель архивирует свой материал.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.post(
            reverse(
                "materials_teacher:materials-teacher-materials-archive",
                kwargs={"pk": self.own_material.id},
            ),
            {
                "confirm": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.own_material.refresh_from_db()

        self.assertEqual(
            self.own_material.status,
            Material.StatusChoices.ARCHIVED,
        )
        self.assertFalse(self.own_material.is_active)

    def test_regular_user_cannot_create_material(self) -> None:
        """
        Пользователь без роли преподавателя не может создать материал.
        """

        self.client.force_authenticate(user=self.regular_user)

        response = self.client.post(
            reverse("materials_teacher:materials-teacher-materials-list"),
            {
                "title": "Материал обычного пользователя",
                "slug": unique_slug("regular-user-material"),
                "material_type": Material.MaterialTypeChoices.TEXT,
                "status": Material.StatusChoices.DRAFT,
                "visibility": Material.VisibilityChoices.PRIVATE,
                "source": Material.SourceChoices.MANUAL,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_teacher_can_log_usage_for_available_material(self) -> None:
        """
        Преподаватель может залогировать использование доступного материала.
        """

        self.client.force_authenticate(user=self.teacher)

        response = self.client.post(
            reverse(
                "materials_teacher:materials-teacher-materials-log-usage",
                kwargs={"pk": self.own_material.id},
            ),
            {
                "action": MaterialUsageLog.ActionChoices.VIEW,
                "context": MaterialUsageLog.ContextChoices.LIBRARY,
                "metadata": {
                    "source": "teacher_test",
                },
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(
            MaterialUsageLog.objects.filter(
                material=self.own_material,
                user=self.teacher,
                action=MaterialUsageLog.ActionChoices.VIEW,
            ).exists()
        )
