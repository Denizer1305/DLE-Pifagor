from __future__ import annotations

from types import SimpleNamespace

from apps.materials.permissions import MaterialPermission
from apps.materials.permissions.shared import (
    user_can_manage_material_object,
    user_can_read_material_object,
)
from apps.materials.tests.factories import (
    create_material,
    create_superadmin,
    create_user,
)
from django.contrib.auth.models import AnonymousUser
from django.test import TestCase


class MaterialPermissionsTestCase(TestCase):
    """
    Тесты ограничений доступа материалов.
    """

    def setUp(self) -> None:
        """
        Подготавливает тестовые данные.
        """

        self.superadmin = create_superadmin()
        self.owner = create_user(email="owner-permissions@example.com")
        self.other_user = create_user(email="other-permissions@example.com")
        self.material = create_material(owner=self.owner)

    def test_anonymous_user_cannot_access_materials(self) -> None:
        """
        Анонимный пользователь не имеет базового доступа к materials API.
        """

        permission = MaterialPermission()
        request = SimpleNamespace(
            method="GET",
            user=AnonymousUser(),
        )

        self.assertFalse(permission.has_permission(request, None))

    def test_superadmin_can_read_material_object(self) -> None:
        """
        Суперадмин может читать материал.
        """

        self.assertTrue(
            user_can_read_material_object(
                user=self.superadmin,
                material=self.material,
            )
        )

    def test_owner_can_manage_own_material_object(self) -> None:
        """
        Владелец может управлять своим материалом на объектном уровне.
        """

        self.assertTrue(
            user_can_manage_material_object(
                user=self.owner,
                material=self.material,
            )
        )

    def test_other_user_cannot_manage_foreign_private_material(self) -> None:
        """
        Пользователь не может управлять чужим приватным материалом.
        """

        self.assertFalse(
            user_can_manage_material_object(
                user=self.other_user,
                material=self.material,
            )
        )

    def test_superadmin_has_write_permission(self) -> None:
        """
        Суперадмин имеет право записи в materials API.
        """

        permission = MaterialPermission()
        request = SimpleNamespace(
            method="POST",
            user=self.superadmin,
        )

        self.assertTrue(permission.has_permission(request, None))
