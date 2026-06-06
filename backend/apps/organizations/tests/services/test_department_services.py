from __future__ import annotations

from apps.organizations.services import (
    create_department,
    deactivate_department,
    restore_department,
    update_department,
)
from apps.organizations.tests.factories import (
    create_department as create_test_department,
)
from apps.organizations.tests.factories import (
    create_organization,
    create_superadmin,
    create_test_user,
)
from django.test import TestCase
from rest_framework.exceptions import PermissionDenied, ValidationError


class DepartmentServicesTestCase(TestCase):
    """
    Тесты сервисов отделений.
    """

    def setUp(self) -> None:
        self.superadmin = create_superadmin(
            email="superadmin-dept-services@example.com",
            phone="+79996100001",
        )
        self.regular_user = create_test_user(
            email="regular-dept-services@example.com",
            phone="+79996100002",
        )
        self.organization = create_organization(
            name="Организация для отделений",
            short_name="ОО",
            code="dept_org",
            slug="dept-org",
        )
        self.department = create_test_department(
            organization=self.organization,
            name="Отделение ИТ",
            short_name="ИТ",
            code="it",
        )

    def test_superadmin_can_create_department(self) -> None:
        """
        Суперадмин может создать отделение.
        """

        department = create_department(
            actor=self.superadmin,
            organization=self.organization,
            data={
                "name": "Экономическое отделение",
                "short_name": "Экономика",
                "code": "economics",
            },
        )

        self.assertEqual(department.organization, self.organization)
        self.assertEqual(department.name, "Экономическое отделение")
        self.assertEqual(department.code, "economics")

    def test_regular_user_cannot_create_department(self) -> None:
        """
        Обычный пользователь не может создать отделение.
        """

        with self.assertRaises(PermissionDenied):
            create_department(
                actor=self.regular_user,
                organization=self.organization,
                data={
                    "name": "Запрещённое отделение",
                    "code": "forbidden",
                },
            )

    def test_superadmin_can_update_department(self) -> None:
        """
        Суперадмин может обновить отделение.
        """

        department = update_department(
            actor=self.superadmin,
            department=self.department,
            data={
                "short_name": "ИТиПО",
                "description": "Новое описание.",
            },
        )

        self.assertEqual(department.short_name, "ИТиПО")
        self.assertEqual(department.description, "Новое описание.")

    def test_regular_user_cannot_update_department(self) -> None:
        """
        Обычный пользователь не может обновить отделение.
        """

        with self.assertRaises(PermissionDenied):
            update_department(
                actor=self.regular_user,
                department=self.department,
                data={
                    "short_name": "Нет доступа",
                },
            )

    def test_deactivate_department(self) -> None:
        """
        Сервис деактивирует отделение.
        """

        department = deactivate_department(
            actor=self.superadmin,
            department=self.department,
        )

        self.assertFalse(department.is_active)

    def test_deactivate_inactive_department_raises_error(self) -> None:
        """
        Повторная деактивация отделения возвращает ошибку.
        """

        self.department.is_active = False
        self.department.save(update_fields=["is_active"])

        with self.assertRaises(ValidationError):
            deactivate_department(
                actor=self.superadmin,
                department=self.department,
            )

    def test_restore_department(self) -> None:
        """
        Сервис восстанавливает отделение.
        """

        self.department.is_active = False
        self.department.save(update_fields=["is_active"])

        department = restore_department(
            actor=self.superadmin,
            department=self.department,
        )

        self.assertTrue(department.is_active)

    def test_cannot_restore_department_of_inactive_organization(self) -> None:
        """
        Нельзя восстановить отделение неактивной организации.
        """

        self.organization.is_active = False
        self.organization.save(update_fields=["is_active"])

        self.department.is_active = False
        self.department.save(update_fields=["is_active"])

        with self.assertRaises(ValidationError):
            restore_department(
                actor=self.superadmin,
                department=self.department,
            )