from __future__ import annotations

from apps.materials.models import Material, MaterialUsageLog, MaterialVersion
from apps.materials.services import archive_material
from apps.materials.services import create_material as service_create_material
from apps.materials.services import (
    create_material_category as service_create_material_category,
)
from apps.materials.services import (
    create_material_version as service_create_material_version,
)
from apps.materials.services import (
    log_material_usage,
    publish_material,
    restore_material,
    set_current_material_version,
)
from apps.materials.tests.factories import create_material as factory_create_material
from apps.materials.tests.factories import (
    create_material_category as factory_create_material_category,
)
from apps.materials.tests.factories import (
    create_material_version as factory_create_material_version,
)
from apps.materials.tests.factories import create_user, unique_slug
from django.test import TestCase


class MaterialServicesTestCase(TestCase):
    """
    Тесты сервисов модуля materials.
    """

    def setUp(self) -> None:
        """
        Подготавливает тестовые данные.
        """

        self.user = create_user(
            email="teacher@example.com",
            role_code="teacher",
        )
        self.category = factory_create_material_category(
            name="Презентации",
            slug=unique_slug("presentations"),
        )
        self.material = factory_create_material(
            title="Основы алгоритмизации",
            slug=unique_slug("algorithms"),
            category=self.category,
            owner=self.user,
            material_type=Material.MaterialTypeChoices.TEXT,
        )

    def test_create_material_category_creates_category(self) -> None:
        """
        Сервис создаёт категорию материалов.
        """

        category = service_create_material_category(
            data={
                "name": "Методические материалы",
                "slug": unique_slug("methods"),
                "description": "Материалы для преподавателя.",
                "is_active": True,
            },
        )

        self.assertEqual(category.name, "Методические материалы")
        self.assertTrue(category.is_active)

    def test_create_material_creates_material(self) -> None:
        """
        Сервис создаёт учебный материал.
        """

        material = service_create_material(
            data={
                "title": "Конспект урока",
                "slug": unique_slug("lesson-notes"),
                "material_type": Material.MaterialTypeChoices.TEXT,
                "visibility": Material.VisibilityChoices.PRIVATE,
                "owner": self.user,
                "category": self.category,
                "tags": [
                    "конспект",
                    "алгоритмы",
                ],
            }
        )

        self.assertEqual(material.title, "Конспект урока")
        self.assertEqual(material.owner, self.user)
        self.assertEqual(material.category, self.category)

    def test_publish_material_sets_status_and_date(self) -> None:
        """
        Публикация материала меняет статус и дату публикации.
        """

        material = publish_material(material=self.material)

        self.assertEqual(material.status, Material.StatusChoices.PUBLISHED)
        self.assertTrue(material.is_active)
        self.assertIsNotNone(material.published_at)

    def test_archive_material_sets_status_and_inactive(self) -> None:
        """
        Архивация материала меняет статус и выключает активность.
        """

        material = archive_material(material=self.material)

        self.assertEqual(material.status, Material.StatusChoices.ARCHIVED)
        self.assertFalse(material.is_active)
        self.assertIsNotNone(material.archived_at)

    def test_restore_material_returns_material_to_draft(self) -> None:
        """
        Восстановление возвращает материал в черновик.
        """

        archive_material(material=self.material)
        self.material.refresh_from_db()

        material = restore_material(material=self.material)

        self.assertEqual(material.status, Material.StatusChoices.DRAFT)
        self.assertTrue(material.is_active)
        self.assertIsNone(material.archived_at)

    def test_create_current_material_version_sets_current_version(self) -> None:
        """
        Создание текущей версии привязывает её к материалу.
        """

        version = service_create_material_version(
            data={
                "material": self.material,
                "version_number": 1,
                "status": MaterialVersion.StatusChoices.CURRENT,
                "content": "Текущая версия материала.",
                "created_by": self.user,
                "is_current": True,
            }
        )

        self.material.refresh_from_db()

        self.assertTrue(version.is_current)
        self.assertEqual(self.material.current_version_id, version.id)

    def test_set_current_material_version_unsets_previous_current(self) -> None:
        """
        Назначение текущей версии снимает флаг с предыдущей.
        """

        first_version = factory_create_material_version(
            material=self.material,
            version_number=1,
            status=MaterialVersion.StatusChoices.CURRENT,
            is_current=True,
        )
        second_version = factory_create_material_version(
            material=self.material,
            version_number=2,
            status=MaterialVersion.StatusChoices.DRAFT,
            is_current=False,
        )

        set_current_material_version(version=second_version)

        first_version.refresh_from_db()
        second_version.refresh_from_db()
        self.material.refresh_from_db()

        self.assertFalse(first_version.is_current)
        self.assertTrue(second_version.is_current)
        self.assertEqual(self.material.current_version_id, second_version.id)

    def test_log_material_usage_creates_usage_log(self) -> None:
        """
        Сервис логирует использование материала.
        """

        usage_log = log_material_usage(
            material=self.material,
            action=MaterialUsageLog.ActionChoices.VIEW,
            context=MaterialUsageLog.ContextChoices.LIBRARY,
            user=self.user,
            metadata={
                "source": "test",
            },
        )

        self.assertEqual(usage_log.material, self.material)
        self.assertEqual(usage_log.user, self.user)
        self.assertEqual(usage_log.action, MaterialUsageLog.ActionChoices.VIEW)
