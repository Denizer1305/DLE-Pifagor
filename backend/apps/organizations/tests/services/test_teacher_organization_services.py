from __future__ import annotations

from apps.organizations.constants import TeacherEmploymentType
from apps.organizations.models import TeacherOrganization
from apps.organizations.services import (
    attach_teacher_to_organization,
    detach_teacher_from_organization,
    set_primary_teacher_organization,
    update_teacher_organization,
)
from apps.organizations.tests.factories import (
    create_organization,
    create_superadmin,
    create_teacher,
    create_teacher_organization,
    create_test_user,
)
from django.test import TestCase
from rest_framework.exceptions import PermissionDenied, ValidationError


class TeacherOrganizationServicesTestCase(TestCase):
    """
    Тесты сервисов связей преподавателей с организациями.
    """

    def setUp(self) -> None:
        self.superadmin = create_superadmin(
            email="superadmin-teacher-org-services@example.com",
            phone="+79996400001",
        )
        self.regular_user = create_test_user(
            email="regular-teacher-org-services@example.com",
            phone="+79996400002",
        )

        self.organization = create_organization(
            name="Организация преподавателей",
            short_name="Преподаватели",
            code="teacher_org",
            slug="teacher-org",
        )
        self.second_organization = create_organization(
            name="Вторая организация преподавателей",
            short_name="Вторая",
            code="second_teacher_org",
            slug="second-teacher-org",
        )

        self.teacher = create_teacher(
            organization=self.organization,
            email="teacher-org-services@example.com",
            phone="+79996400003",
            first_name="Иван",
            last_name="Иванов",
            position="Преподаватель",
        )

        self.teacher_organization = create_teacher_organization(
            teacher=self.teacher,
            organization=self.organization,
            position="Преподаватель математики",
            employment_type=TeacherEmploymentType.FULL_TIME,
            is_primary=True,
            is_active=True,
        )

    def test_attach_teacher_to_organization(self) -> None:
        """
        Сервис привязывает преподавателя к организации.
        """

        self.teacher_organization.delete()

        teacher_organization = attach_teacher_to_organization(
            actor=self.superadmin,
            teacher=self.teacher,
            organization=self.organization,
            data={
                "position": "Преподаватель информатики",
                "employment_type": TeacherEmploymentType.FULL_TIME,
                "is_primary": True,
            },
        )

        self.assertEqual(teacher_organization.teacher, self.teacher)
        self.assertEqual(teacher_organization.organization, self.organization)
        self.assertEqual(
            teacher_organization.position,
            "Преподаватель информатики",
        )
        self.assertTrue(teacher_organization.is_primary)

    def test_regular_user_cannot_attach_teacher_to_organization(self) -> None:
        """
        Обычный пользователь не может привязать преподавателя к организации.
        """

        self.teacher_organization.delete()

        with self.assertRaises(PermissionDenied):
            attach_teacher_to_organization(
                actor=self.regular_user,
                teacher=self.teacher,
                organization=self.organization,
                data={
                    "position": "Преподаватель",
                },
            )

    def test_cannot_attach_user_without_teacher_role(self) -> None:
        """
        Пользователя без роли преподавателя нельзя привязать как преподавателя.
        """

        not_teacher = create_test_user(
            email="not-teacher-services@example.com",
            phone="+79996400004",
        )

        with self.assertRaises(ValidationError):
            attach_teacher_to_organization(
                actor=self.superadmin,
                teacher=not_teacher,
                organization=self.organization,
                data={
                    "position": "Не преподаватель",
                },
            )

        self.assertFalse(
            TeacherOrganization.objects.filter(
                teacher=not_teacher,
                organization=self.organization,
            ).exists()
        )

    def test_update_teacher_organization(self) -> None:
        """
        Сервис обновляет связь преподавателя с организацией.
        """

        teacher_organization = update_teacher_organization(
            actor=self.superadmin,
            teacher_organization=self.teacher_organization,
            data={
                "position": "Старший преподаватель",
                "employment_type": TeacherEmploymentType.PART_TIME,
                "notes": "Обновлено сервисом.",
            },
        )

        self.assertEqual(teacher_organization.position, "Старший преподаватель")
        self.assertEqual(
            teacher_organization.employment_type,
            TeacherEmploymentType.PART_TIME,
        )
        self.assertEqual(teacher_organization.notes, "Обновлено сервисом.")

    def test_regular_user_cannot_update_teacher_organization(self) -> None:
        """
        Обычный пользователь не может обновить связь преподавателя.
        """

        with self.assertRaises(PermissionDenied):
            update_teacher_organization(
                actor=self.regular_user,
                teacher_organization=self.teacher_organization,
                data={
                    "position": "Нет доступа",
                },
            )

    def test_detach_teacher_from_organization(self) -> None:
        """
        Сервис деактивирует связь преподавателя с организацией.
        """

        teacher_organization = detach_teacher_from_organization(
            actor=self.superadmin,
            teacher_organization=self.teacher_organization,
        )

        self.assertFalse(teacher_organization.is_active)
        self.assertFalse(teacher_organization.is_primary)

    def test_detach_inactive_teacher_organization_raises_error(self) -> None:
        """
        Повторная деактивация связи возвращает ошибку.
        """

        self.teacher_organization.is_active = False
        self.teacher_organization.is_primary = False
        self.teacher_organization.save(
            update_fields=[
                "is_active",
                "is_primary",
            ]
        )

        with self.assertRaises(ValidationError):
            detach_teacher_from_organization(
                actor=self.superadmin,
                teacher_organization=self.teacher_organization,
            )

    def test_set_primary_teacher_organization(self) -> None:
        """
        Сервис делает связь основной и снимает primary с другой связи.
        """

        second_relation = create_teacher_organization(
            teacher=self.teacher,
            organization=self.second_organization,
            position="Преподаватель",
            employment_type=TeacherEmploymentType.PART_TIME,
            is_primary=False,
            is_active=True,
        )

        teacher_organization = set_primary_teacher_organization(
            actor=self.superadmin,
            teacher_organization=second_relation,
        )

        self.teacher_organization.refresh_from_db()

        self.assertTrue(teacher_organization.is_primary)
        self.assertFalse(self.teacher_organization.is_primary)

    def test_cannot_set_inactive_teacher_organization_as_primary(self) -> None:
        """
        Неактивную связь нельзя сделать основной.
        """

        self.teacher_organization.is_active = False
        self.teacher_organization.is_primary = False
        self.teacher_organization.save(
            update_fields=[
                "is_active",
                "is_primary",
            ]
        )

        with self.assertRaises(ValidationError):
            set_primary_teacher_organization(
                actor=self.superadmin,
                teacher_organization=self.teacher_organization,
            )
