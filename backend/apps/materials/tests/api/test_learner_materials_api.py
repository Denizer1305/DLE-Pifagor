from __future__ import annotations

from apps.materials.models import Material, MaterialUsageLog
from apps.materials.tests.factories import create_material as factory_create_material
from apps.materials.tests.factories import (
    create_material_usage_log,
    create_user,
    extract_results,
    unique_slug,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class LearnerMaterialsApiTestCase(APITestCase):
    """
    API-тесты материалов обучающегося.
    """

    def setUp(self) -> None:
        """
        Подготавливает тестовые данные.
        """

        self.learner = create_user(
            email="materials-learner@example.com",
            role_code="learner",
        )
        self.other_user = create_user(
            email="materials-other-user@example.com",
        )

        self.own_material = factory_create_material(
            title="Личный материал обучающегося",
            slug=unique_slug("learner-own-material"),
            owner=self.learner,
            material_type=Material.MaterialTypeChoices.TEXT,
            visibility=Material.VisibilityChoices.PRIVATE,
            status=Material.StatusChoices.DRAFT,
            is_active=True,
        )
        self.public_material = factory_create_material(
            title="Публичный материал",
            slug=unique_slug("learner-public-material"),
            material_type=Material.MaterialTypeChoices.TEXT,
            visibility=Material.VisibilityChoices.PUBLIC,
            status=Material.StatusChoices.PUBLISHED,
            is_active=True,
        )
        self.foreign_private_material = factory_create_material(
            title="Чужой закрытый материал",
            slug=unique_slug("learner-foreign-private-material"),
            owner=self.other_user,
            material_type=Material.MaterialTypeChoices.TEXT,
            visibility=Material.VisibilityChoices.PRIVATE,
            status=Material.StatusChoices.DRAFT,
            is_active=True,
        )
        self.archived_public_material = factory_create_material(
            title="Архивный публичный материал",
            slug=unique_slug("learner-archived-public-material"),
            material_type=Material.MaterialTypeChoices.TEXT,
            visibility=Material.VisibilityChoices.PUBLIC,
            status=Material.StatusChoices.ARCHIVED,
            is_active=False,
        )

    def test_learner_can_get_available_materials_list(self) -> None:
        """
        Обучающийся видит свои материалы и публичные опубликованные материалы.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.get(
            reverse("materials_learner:materials-learner-materials-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        material_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.own_material.id, material_ids)
        self.assertIn(self.public_material.id, material_ids)
        self.assertNotIn(self.foreign_private_material.id, material_ids)
        self.assertNotIn(self.archived_public_material.id, material_ids)

    def test_learner_can_get_public_material_detail(self) -> None:
        """
        Обучающийся может открыть публичный опубликованный материал.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.get(
            reverse(
                "materials_learner:materials-learner-materials-detail",
                kwargs={"pk": self.public_material.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], self.public_material.id)

    def test_learner_can_get_own_material_detail(self) -> None:
        """
        Обучающийся может открыть свой материал.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.get(
            reverse(
                "materials_learner:materials-learner-materials-detail",
                kwargs={"pk": self.own_material.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["id"], self.own_material.id)

    def test_learner_cannot_get_foreign_private_material_detail(self) -> None:
        """
        Обучающийся не может открыть чужой приватный материал.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.get(
            reverse(
                "materials_learner:materials-learner-materials-detail",
                kwargs={"pk": self.foreign_private_material.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_learner_cannot_create_material(self) -> None:
        """
        Обучающийся не может создавать материалы через learner API.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.post(
            reverse("materials_learner:materials-learner-materials-list"),
            {
                "title": "Материал обучающегося",
                "slug": unique_slug("learner-created-material"),
                "material_type": Material.MaterialTypeChoices.TEXT,
                "status": Material.StatusChoices.DRAFT,
                "visibility": Material.VisibilityChoices.PRIVATE,
                "source": Material.SourceChoices.MANUAL,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_learner_cannot_update_own_material(self) -> None:
        """
        Обучающийся не может изменять материалы через learner API.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.patch(
            reverse(
                "materials_learner:materials-learner-materials-detail",
                kwargs={"pk": self.own_material.id},
            ),
            {
                "title": "Попытка изменить материал",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        self.own_material.refresh_from_db()

        self.assertEqual(
            self.own_material.title,
            "Личный материал обучающегося",
        )

    def test_learner_cannot_publish_material(self) -> None:
        """
        Обучающийся не может публиковать материалы.
        """

        self.client.force_authenticate(user=self.learner)

        response = self.client.post(
            reverse(
                "materials_learner:materials-learner-materials-publish",
                kwargs={"pk": self.own_material.id},
            ),
            {
                "confirm": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_learner_can_get_usage_logs_list(self) -> None:
        """
        Обучающийся получает доступные события журнала использования материалов.
        """

        own_usage_log = create_material_usage_log(
            material=self.own_material,
            user=self.learner,
            action=MaterialUsageLog.ActionChoices.VIEW,
            context=MaterialUsageLog.ContextChoices.LIBRARY,
        )
        public_usage_log = create_material_usage_log(
            material=self.public_material,
            user=self.other_user,
            action=MaterialUsageLog.ActionChoices.VIEW,
            context=MaterialUsageLog.ContextChoices.LIBRARY,
        )
        foreign_private_usage_log = create_material_usage_log(
            material=self.foreign_private_material,
            user=self.other_user,
            action=MaterialUsageLog.ActionChoices.VIEW,
            context=MaterialUsageLog.ContextChoices.LIBRARY,
        )

        self.client.force_authenticate(user=self.learner)

        response = self.client.get(
            reverse("materials_learner:materials-learner-usage-logs-list")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        usage_log_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(own_usage_log.id, usage_log_ids)
        self.assertIn(public_usage_log.id, usage_log_ids)
        self.assertNotIn(foreign_private_usage_log.id, usage_log_ids)

    def test_anonymous_user_cannot_get_learner_materials_list(self) -> None:
        """
        Анонимный пользователь не имеет доступа к learner API материалов.
        """

        response = self.client.get(
            reverse("materials_learner:materials-learner-materials-list")
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
