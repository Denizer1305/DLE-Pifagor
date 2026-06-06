from __future__ import annotations

from apps.organizations.constants import StudyGroupStatus
from apps.organizations.services import (
    archive_study_group,
    create_study_group,
    restore_study_group,
    update_study_group,
)
from apps.organizations.tests.factories import (
    create_department,
    create_organization,
    create_study_group as create_test_study_group,
    create_superadmin,
    create_test_user,
)
from django.test import TestCase
from rest_framework.exceptions import PermissionDenied, ValidationError


class StudyGroupServicesTestCase(TestCase):
    """
    Тесты сервисов учебных групп.
    """

    def setUp(self) -> None:
        self.superadmin = create_superadmin(
            email="superadmin-group-services@example.com",
            phone="+79996200001",
        )
        self.regular_user = create_test_user(
            email="regular-group-services@example.com",
            phone="+79996200002",
        )
        self.organization = create_organization(
            name="Организация для групп",
            short_name="ОО",
            code="group_org",
            slug="group-org",
        )
        self.department = create_department(
            organization=self.organization,
            name="Отделение ИТ",
            short_name="ИТ",
            code="it",
        )
        self.group = create_test_study_group(
            organization=self.organization,
            department=self.department,
            name="ИС-21",
            code="is_21",
        )

    def test_superadmin_can_create_study_group(self) -> None:
        """
        Суперадмин может создать учебную группу.
        """

        group = create_study_group(
            actor=self.superadmin,
            organization=self.organization,
            data={
                "department": self.department,
                "name": "ИС-22",
                "code": "is_22",
                "admission_year": 2024,
                "graduation_year": 2028,
                "course_number": 1,
            },
        )

        self.assertEqual(group.organization, self.organization)
        self.assertEqual(group.department, self.department)
        self.assertEqual(group.name, "ИС-22")
        self.assertTrue(group.is_active)

    def test_regular_user_cannot_create_study_group(self) -> None:
        """
        Обычный пользователь не может создать учебную группу.
        """

        with self.assertRaises(PermissionDenied):
            create_study_group(
                actor=self.regular_user,
                organization=self.organization,
                data={
                    "department": self.department,
                    "name": "ИС-23",
                    "code": "is_23",
                },
            )

    def test_cannot_create_group_with_foreign_department(self) -> None:
        """
        Нельзя создать группу с отделением другой организации.
        """

        other_organization = create_organization(
            name="Другая организация",
            short_name="Другая",
            code="other_group_org",
            slug="other-group-org",
        )
        foreign_department = create_department(
            organization=other_organization,
            name="Чужое отделение",
            short_name="Чужое",
            code="foreign",
        )

        with self.assertRaises(ValidationError):
            create_study_group(
                actor=self.superadmin,
                organization=self.organization,
                data={
                    "department": foreign_department,
                    "name": "ИС-24",
                    "code": "is_24",
                },
            )

    def test_superadmin_can_update_study_group(self) -> None:
        """
        Суперадмин может обновить учебную группу.
        """

        group = update_study_group(
            actor=self.superadmin,
            group=self.group,
            data={
                "course_number": 3,
                "description": "Новое описание группы.",
            },
        )

        self.assertEqual(group.course_number, 3)
        self.assertEqual(group.description, "Новое описание группы.")

    def test_regular_user_cannot_update_study_group(self) -> None:
        """
        Обычный пользователь не может обновить учебную группу.
        """

        with self.assertRaises(PermissionDenied):
            update_study_group(
                actor=self.regular_user,
                group=self.group,
                data={
                    "course_number": 3,
                },
            )

    def test_archive_study_group(self) -> None:
        """
        Сервис архивирует учебную группу.
        """

        group = archive_study_group(
            actor=self.superadmin,
            group=self.group,
        )

        self.assertEqual(group.status, StudyGroupStatus.ARCHIVED)
        self.assertFalse(group.is_active)
        self.assertTrue(group.is_archived)

    def test_archive_archived_group_raises_error(self) -> None:
        """
        Повторное архивирование группы возвращает ошибку.
        """

        self.group.status = StudyGroupStatus.ARCHIVED
        self.group.save()

        with self.assertRaises(ValidationError):
            archive_study_group(
                actor=self.superadmin,
                group=self.group,
            )

    def test_restore_study_group(self) -> None:
        """
        Сервис восстанавливает учебную группу.
        """

        self.group.status = StudyGroupStatus.ARCHIVED
        self.group.save()

        group = restore_study_group(
            actor=self.superadmin,
            group=self.group,
        )

        self.assertEqual(group.status, StudyGroupStatus.ACTIVE)
        self.assertTrue(group.is_active)
        self.assertFalse(group.is_archived)

    def test_cannot_restore_group_of_inactive_organization(self) -> None:
        """
        Нельзя восстановить группу неактивной организации.
        """

        self.organization.is_active = False
        self.organization.save(update_fields=["is_active"])

        self.group.status = StudyGroupStatus.ARCHIVED
        self.group.save()

        with self.assertRaises(ValidationError):
            restore_study_group(
                actor=self.superadmin,
                group=self.group,
            )