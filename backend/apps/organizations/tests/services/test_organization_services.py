from __future__ import annotations

from apps.organizations.services import (
    create_organization,
    deactivate_organization,
    restore_organization,
    update_organization,
)
from apps.organizations.tests.factories import (
    create_organization as create_test_organization,
)
from apps.organizations.tests.factories import create_superadmin, create_test_user
from django.test import TestCase
from rest_framework.exceptions import PermissionDenied, ValidationError


class OrganizationServicesTestCase(TestCase):
    """
    Тесты сервисов образовательных организаций.
    """

    def setUp(self) -> None:
        self.superadmin = create_superadmin(
            email="superadmin-org-services@example.com",
            phone="+79996000001",
        )
        self.regular_user = create_test_user(
            email="regular-org-services@example.com",
            phone="+79996000002",
        )
        self.organization = create_test_organization(
            name="Основная организация",
            short_name="Основная",
            code="main_org",
            slug="main-org",
        )

    def test_superadmin_can_create_organization(self) -> None:
        """
        Суперадмин может создать организацию через сервис.
        """

        organization = create_organization(
            actor=self.superadmin,
            data={
                "name": "Новая организация",
                "short_name": "Новая",
                "code": "new_org",
                "slug": "new-org",
                "city": "Владимир",
                "is_public": True,
            },
        )

        self.assertEqual(organization.name, "Новая организация")
        self.assertEqual(organization.code, "new_org")
        self.assertTrue(organization.is_active)

    def test_regular_user_cannot_create_organization(self) -> None:
        """
        Обычный пользователь не может создать организацию.
        """

        with self.assertRaises(PermissionDenied):
            create_organization(
                actor=self.regular_user,
                data={
                    "name": "Запрещённая организация",
                    "code": "forbidden_org",
                },
            )

    def test_superadmin_can_update_organization(self) -> None:
        """
        Суперадмин может обновить организацию.
        """

        organization = update_organization(
            actor=self.superadmin,
            organization=self.organization,
            data={
                "city": "Суздаль",
                "is_public": False,
            },
        )

        self.assertEqual(organization.city, "Суздаль")
        self.assertFalse(organization.is_public)

    def test_regular_user_cannot_update_organization(self) -> None:
        """
        Обычный пользователь не может обновить организацию.
        """

        with self.assertRaises(PermissionDenied):
            update_organization(
                actor=self.regular_user,
                organization=self.organization,
                data={
                    "city": "Суздаль",
                },
            )

    def test_deactivate_organization(self) -> None:
        """
        Сервис деактивирует организацию.
        """

        organization = deactivate_organization(
            actor=self.superadmin,
            organization=self.organization,
        )

        self.assertFalse(organization.is_active)

    def test_deactivate_already_inactive_organization_raises_error(self) -> None:
        """
        Повторная деактивация организации возвращает ошибку.
        """

        self.organization.is_active = False
        self.organization.save(update_fields=["is_active"])

        with self.assertRaises(ValidationError):
            deactivate_organization(
                actor=self.superadmin,
                organization=self.organization,
            )

    def test_restore_organization(self) -> None:
        """
        Сервис восстанавливает организацию.
        """

        self.organization.is_active = False
        self.organization.save(update_fields=["is_active"])

        organization = restore_organization(
            actor=self.superadmin,
            organization=self.organization,
        )

        self.assertTrue(organization.is_active)

    def test_restore_active_organization_raises_error(self) -> None:
        """
        Повторное восстановление активной организации возвращает ошибку.
        """

        with self.assertRaises(ValidationError):
            restore_organization(
                actor=self.superadmin,
                organization=self.organization,
            )
