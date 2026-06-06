from __future__ import annotations

from apps.organizations.services import (
    clear_group_join_code,
    clear_teacher_registration_code,
    disable_group_join_code,
    disable_teacher_registration_code,
    set_group_join_code,
    set_teacher_registration_code,
    verify_group_join_code,
    verify_teacher_registration_code,
)
from apps.organizations.tests.factories import (
    create_department,
    create_organization,
    create_study_group,
    create_superadmin,
    create_test_user,
)
from django.test import TestCase
from rest_framework.exceptions import PermissionDenied, ValidationError


class CodeServicesTestCase(TestCase):
    """
    Тесты сервисов кодов организаций и групп.
    """

    def setUp(self) -> None:
        self.superadmin = create_superadmin(
            email="superadmin-code-services@example.com",
            phone="+79996300001",
        )
        self.regular_user = create_test_user(
            email="regular-code-services@example.com",
            phone="+79996300002",
        )
        self.organization = create_organization(
            name="Организация для кодов",
            short_name="Коды",
            code="code_org",
            slug="code-org",
        )
        self.department = create_department(
            organization=self.organization,
            name="Отделение кодов",
            short_name="Коды",
            code="codes",
        )
        self.group = create_study_group(
            organization=self.organization,
            department=self.department,
            name="КОД-1",
            code="code_1",
        )

    def test_set_teacher_registration_code(self) -> None:
        """
        Сервис устанавливает код регистрации преподавателя.
        """

        organization, raw_code = set_teacher_registration_code(
            actor=self.superadmin,
            organization=self.organization,
            raw_code="teacher-code-123",
        )

        self.assertEqual(raw_code, "teacher-code-123")
        self.assertTrue(organization.has_active_teacher_registration_code)
        self.assertTrue(
            verify_teacher_registration_code(
                organization=organization,
                raw_code="teacher-code-123",
            )
        )

    def test_regular_user_cannot_set_teacher_registration_code(self) -> None:
        """
        Обычный пользователь не может установить код регистрации преподавателя.
        """

        with self.assertRaises(PermissionDenied):
            set_teacher_registration_code(
                actor=self.regular_user,
                organization=self.organization,
                raw_code="teacher-code-123",
            )

    def test_too_short_teacher_registration_code_raises_error(self) -> None:
        """
        Слишком короткий код регистрации преподавателя возвращает ошибку.
        """

        with self.assertRaises(ValidationError):
            set_teacher_registration_code(
                actor=self.superadmin,
                organization=self.organization,
                raw_code="123",
            )

    def test_disable_teacher_registration_code(self) -> None:
        """
        Сервис отключает код регистрации преподавателя.
        """

        self.organization.set_teacher_registration_code(
            "teacher-code-123",
            save=True,
        )

        organization = disable_teacher_registration_code(
            actor=self.superadmin,
            organization=self.organization,
        )

        self.assertFalse(organization.teacher_registration_code_is_active)

    def test_clear_teacher_registration_code(self) -> None:
        """
        Сервис очищает код регистрации преподавателя.
        """

        self.organization.set_teacher_registration_code(
            "teacher-code-123",
            save=True,
        )

        organization = clear_teacher_registration_code(
            actor=self.superadmin,
            organization=self.organization,
        )

        self.assertEqual(organization.teacher_registration_code_hash, "")
        self.assertFalse(organization.teacher_registration_code_is_active)
        self.assertIsNone(organization.teacher_registration_code_expires_at)

    def test_set_group_join_code(self) -> None:
        """
        Сервис устанавливает код вступления в группу.
        """

        group, raw_code = set_group_join_code(
            actor=self.superadmin,
            group=self.group,
            raw_code="group-code-123",
        )

        self.assertEqual(raw_code, "group-code-123")
        self.assertTrue(group.has_active_join_code)
        self.assertTrue(
            verify_group_join_code(
                group=group,
                raw_code="group-code-123",
            )
        )

    def test_regular_user_cannot_set_group_join_code(self) -> None:
        """
        Обычный пользователь не может установить код вступления в группу.
        """

        with self.assertRaises(PermissionDenied):
            set_group_join_code(
                actor=self.regular_user,
                group=self.group,
                raw_code="group-code-123",
            )

    def test_too_short_group_join_code_raises_error(self) -> None:
        """
        Слишком короткий код вступления в группу возвращает ошибку.
        """

        with self.assertRaises(ValidationError):
            set_group_join_code(
                actor=self.superadmin,
                group=self.group,
                raw_code="123",
            )

    def test_disable_group_join_code(self) -> None:
        """
        Сервис отключает код вступления в группу.
        """

        self.group.set_join_code(
            "group-code-123",
            save=True,
        )

        group = disable_group_join_code(
            actor=self.superadmin,
            group=self.group,
        )

        self.assertFalse(group.join_code_is_active)

    def test_clear_group_join_code(self) -> None:
        """
        Сервис очищает код вступления в группу.
        """

        self.group.set_join_code(
            "group-code-123",
            save=True,
        )

        group = clear_group_join_code(
            actor=self.superadmin,
            group=self.group,
        )

        self.assertEqual(group.join_code_hash, "")
        self.assertFalse(group.join_code_is_active)
        self.assertIsNone(group.join_code_expires_at)