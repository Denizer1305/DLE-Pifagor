from __future__ import annotations

from apps.materials.models import Material
from apps.materials.selectors import (
    get_material_by_id,
    get_material_by_slug,
    get_published_public_materials,
    get_user_available_materials,
    material_list_queryset,
)
from apps.materials.tests.factories import (
    create_material,
    create_superadmin,
    create_user,
    unique_slug,
)
from django.test import TestCase


class MaterialSelectorsTestCase(TestCase):
    """
    Тесты селекторов материалов.
    """

    def setUp(self) -> None:
        """
        Подготавливает тестовые данные.
        """

        self.superadmin = create_superadmin()
        self.owner = create_user(email="owner@example.com")
        self.other_user = create_user(email="other@example.com")

        self.private_material = create_material(
            title="Закрытый материал по алгоритмам",
            slug=unique_slug("private-algorithms"),
            owner=self.owner,
            visibility=Material.VisibilityChoices.PRIVATE,
            status=Material.StatusChoices.DRAFT,
        )
        self.public_material = create_material(
            title="Публичная презентация",
            slug=unique_slug("public-presentation"),
            visibility=Material.VisibilityChoices.PUBLIC,
            status=Material.StatusChoices.PUBLISHED,
            is_active=True,
        )

    def test_get_material_by_id_returns_material(self) -> None:
        """
        Селектор возвращает материал по id.
        """

        material = get_material_by_id(self.private_material.id)

        self.assertEqual(material.id, self.private_material.id)

    def test_get_material_by_slug_returns_material(self) -> None:
        """
        Селектор возвращает материал по slug.
        """

        material = get_material_by_slug(self.private_material.slug)

        self.assertEqual(material.id, self.private_material.id)

    def test_material_list_queryset_filters_by_search(self) -> None:
        """
        Список материалов фильтруется по поиску.
        """

        queryset = material_list_queryset(search="алгоритм")

        self.assertIn(self.private_material, queryset)
        self.assertNotIn(self.public_material, queryset)

    def test_superadmin_available_materials_contains_all(self) -> None:
        """
        Суперадмин видит все материалы.
        """

        queryset = get_user_available_materials(user=self.superadmin)

        self.assertIn(self.private_material, queryset)
        self.assertIn(self.public_material, queryset)

    def test_regular_user_sees_public_and_owned_materials_only(self) -> None:
        """
        Обычный пользователь видит публичные и свои материалы.
        """

        owned_material = create_material(
            title="Собственный материал",
            slug=unique_slug("owned"),
            owner=self.other_user,
            visibility=Material.VisibilityChoices.PRIVATE,
        )

        queryset = get_user_available_materials(user=self.other_user)

        self.assertIn(owned_material, queryset)
        self.assertIn(self.public_material, queryset)
        self.assertNotIn(self.private_material, queryset)

    def test_get_published_public_materials_returns_only_public_published(self) -> None:
        """
        Публичный селектор возвращает только опубликованные публичные материалы.
        """

        queryset = get_published_public_materials()

        self.assertIn(self.public_material, queryset)
        self.assertNotIn(self.private_material, queryset)
