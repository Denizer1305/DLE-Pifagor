from __future__ import annotations

from apps.materials.models import Material, MaterialVersion
from apps.materials.services import archive_material_version
from apps.materials.services import (
    create_material_version as service_create_material_version,
)
from apps.materials.services import (
    set_current_material_version,
    update_material_version,
)
from apps.materials.tests.factories import create_material as factory_create_material
from apps.materials.tests.factories import (
    create_material_version as factory_create_material_version,
)
from apps.materials.tests.factories import create_user, unique_slug
from django.test import TestCase


class MaterialVersionServicesTestCase(TestCase):
    """
    Тесты сервисов версий учебных материалов.
    """

    def setUp(self) -> None:
        """
        Подготавливает тестовые данные.
        """

        self.teacher = create_user(
            email="version-teacher@example.com",
            role_code="teacher",
        )
        self.material = factory_create_material(
            title="Материал по алгоритмам",
            slug=unique_slug("algorithm-material"),
            material_type=Material.MaterialTypeChoices.TEXT,
            owner=self.teacher,
        )

    def test_create_material_version_creates_version(self) -> None:
        """
        Сервис создаёт версию материала.
        """

        version = service_create_material_version(
            data={
                "material": self.material,
                "version_number": 1,
                "status": MaterialVersion.StatusChoices.DRAFT,
                "content": "Первая версия материала.",
                "created_by": self.teacher,
                "change_log": "Создана первая версия.",
                "is_current": False,
            }
        )

        self.assertEqual(version.material, self.material)
        self.assertEqual(version.version_number, 1)
        self.assertEqual(version.content, "Первая версия материала.")
        self.assertEqual(version.created_by, self.teacher)
        self.assertFalse(version.is_current)

    def test_create_current_material_version_updates_material_current_version(
        self,
    ) -> None:
        """
        Создание текущей версии обновляет current_version у материала.
        """

        version = service_create_material_version(
            data={
                "material": self.material,
                "version_number": 1,
                "status": MaterialVersion.StatusChoices.CURRENT,
                "content": "Текущая версия материала.",
                "created_by": self.teacher,
                "is_current": True,
            }
        )

        self.material.refresh_from_db()

        self.assertTrue(version.is_current)
        self.assertEqual(version.status, MaterialVersion.StatusChoices.CURRENT)
        self.assertEqual(self.material.current_version_id, version.id)

    def test_set_current_material_version_unsets_previous_current_version(
        self,
    ) -> None:
        """
        Назначение новой текущей версии снимает флаг с предыдущей.
        """

        first_version = factory_create_material_version(
            material=self.material,
            version_number=1,
            status=MaterialVersion.StatusChoices.CURRENT,
            content="Первая версия.",
            is_current=True,
        )
        second_version = factory_create_material_version(
            material=self.material,
            version_number=2,
            status=MaterialVersion.StatusChoices.DRAFT,
            content="Вторая версия.",
            is_current=False,
        )

        set_current_material_version(version=second_version)

        first_version.refresh_from_db()
        second_version.refresh_from_db()
        self.material.refresh_from_db()

        self.assertFalse(first_version.is_current)
        self.assertEqual(
            first_version.status,
            MaterialVersion.StatusChoices.ARCHIVED,
        )
        self.assertTrue(second_version.is_current)
        self.assertEqual(
            second_version.status,
            MaterialVersion.StatusChoices.CURRENT,
        )
        self.assertEqual(self.material.current_version_id, second_version.id)

    def test_update_material_version_changes_content_and_change_log(self) -> None:
        """
        Сервис обновляет содержимое и описание изменений версии.
        """

        version = factory_create_material_version(
            material=self.material,
            version_number=1,
            status=MaterialVersion.StatusChoices.DRAFT,
            content="Старое содержимое.",
        )

        updated_version = update_material_version(
            version=version,
            data={
                "content": "Обновлённое содержимое.",
                "change_log": "Исправлен текст материала.",
            },
        )

        self.assertEqual(updated_version.content, "Обновлённое содержимое.")
        self.assertEqual(
            updated_version.change_log,
            "Исправлен текст материала.",
        )

    def test_update_material_version_to_current_updates_material(self) -> None:
        """
        Обновление версии до текущей привязывает её к материалу.
        """

        version = factory_create_material_version(
            material=self.material,
            version_number=1,
            status=MaterialVersion.StatusChoices.DRAFT,
            content="Черновая версия.",
            is_current=False,
        )

        updated_version = update_material_version(
            version=version,
            data={
                "status": MaterialVersion.StatusChoices.CURRENT,
                "is_current": True,
            },
        )

        self.material.refresh_from_db()

        self.assertTrue(updated_version.is_current)
        self.assertEqual(
            updated_version.status,
            MaterialVersion.StatusChoices.CURRENT,
        )
        self.assertEqual(self.material.current_version_id, updated_version.id)

    def test_archive_material_version_changes_status(self) -> None:
        """
        Архивация версии меняет статус и снимает флаг текущей версии.
        """

        version = factory_create_material_version(
            material=self.material,
            version_number=1,
            status=MaterialVersion.StatusChoices.CURRENT,
            content="Текущая версия.",
            is_current=True,
        )

        archived_version = archive_material_version(version=version)

        self.assertEqual(
            archived_version.status,
            MaterialVersion.StatusChoices.ARCHIVED,
        )
        self.assertFalse(archived_version.is_current)

    def test_archive_current_material_version_clears_material_current_version(
        self,
    ) -> None:
        """
        Архивация текущей версии очищает current_version у материала.
        """

        version = service_create_material_version(
            data={
                "material": self.material,
                "version_number": 1,
                "status": MaterialVersion.StatusChoices.CURRENT,
                "content": "Текущая версия.",
                "created_by": self.teacher,
                "is_current": True,
            }
        )

        archive_material_version(version=version)

        self.material.refresh_from_db()
        version.refresh_from_db()

        self.assertIsNone(self.material.current_version_id)
        self.assertEqual(
            version.status,
            MaterialVersion.StatusChoices.ARCHIVED,
        )
        self.assertFalse(version.is_current)
