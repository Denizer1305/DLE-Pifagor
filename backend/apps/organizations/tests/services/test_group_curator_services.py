from __future__ import annotations

from apps.organizations.models import GroupCurator
from apps.organizations.services import (
    assign_group_curator,
    remove_group_curator,
    set_primary_group_curator,
    update_group_curator,
)
from apps.organizations.tests.factories import (
    create_department,
    create_group_curator,
    create_organization,
    create_study_group,
    create_superadmin,
    create_teacher,
    create_test_user,
)
from django.test import TestCase
from rest_framework.exceptions import PermissionDenied, ValidationError


class GroupCuratorServicesTestCase(TestCase):
    """
    Тесты сервисов кураторов групп.
    """

    def setUp(self) -> None:
        self.superadmin = create_superadmin(
            email="superadmin-curator-services@example.com",
            phone="+79996500001",
        )
        self.regular_user = create_test_user(
            email="regular-curator-services@example.com",
            phone="+79996500002",
        )

        self.organization = create_organization(
            name="Организация кураторов",
            short_name="Кураторы",
            code="curator_org",
            slug="curator-org",
        )
        self.department = create_department(
            organization=self.organization,
            name="Отделение кураторов",
            short_name="Кураторы",
            code="curators",
        )
        self.group = create_study_group(
            organization=self.organization,
            department=self.department,
            name="КУР-1",
            code="cur_1",
        )
        self.second_group = create_study_group(
            organization=self.organization,
            department=self.department,
            name="КУР-2",
            code="cur_2",
        )

        self.teacher = create_teacher(
            organization=self.organization,
            email="curator-teacher-services@example.com",
            phone="+79996500003",
            first_name="Иван",
            last_name="Иванов",
            position="Преподаватель",
        )
        self.second_teacher = create_teacher(
            organization=self.organization,
            email="second-curator-teacher-services@example.com",
            phone="+79996500004",
            first_name="Пётр",
            last_name="Петров",
            position="Преподаватель",
        )

        self.group_curator = create_group_curator(
            group=self.group,
            teacher=self.teacher,
            is_primary=True,
            is_active=True,
        )

    def test_assign_group_curator(self) -> None:
        """
        Сервис назначает куратора группе.
        """

        group_curator = assign_group_curator(
            actor=self.superadmin,
            group=self.second_group,
            teacher=self.second_teacher,
            data={
                "is_primary": True,
                "notes": "Назначен сервисом.",
            },
        )

        self.assertEqual(group_curator.group, self.second_group)
        self.assertEqual(group_curator.teacher, self.second_teacher)
        self.assertTrue(group_curator.is_primary)
        self.assertEqual(group_curator.notes, "Назначен сервисом.")

    def test_regular_user_cannot_assign_group_curator(self) -> None:
        """
        Обычный пользователь не может назначить куратора.
        """

        with self.assertRaises(PermissionDenied):
            assign_group_curator(
                actor=self.regular_user,
                group=self.second_group,
                teacher=self.second_teacher,
                data={
                    "is_primary": True,
                },
            )

    def test_cannot_assign_user_without_teacher_role_as_curator(self) -> None:
        """
        Пользователя без роли преподавателя нельзя назначить куратором.
        """

        not_teacher = create_test_user(
            email="not-curator-services@example.com",
            phone="+79996500005",
        )

        with self.assertRaises(ValidationError):
            assign_group_curator(
                actor=self.superadmin,
                group=self.second_group,
                teacher=not_teacher,
                data={
                    "is_primary": True,
                },
            )

        self.assertFalse(
            GroupCurator.objects.filter(
                group=self.second_group,
                teacher=not_teacher,
            ).exists()
        )

    def test_update_group_curator(self) -> None:
        """
        Сервис обновляет связь куратора с группой.
        """

        group_curator = update_group_curator(
            actor=self.superadmin,
            group_curator=self.group_curator,
            data={
                "is_primary": False,
                "notes": "Обновлено сервисом.",
            },
        )

        self.assertFalse(group_curator.is_primary)
        self.assertEqual(group_curator.notes, "Обновлено сервисом.")

    def test_regular_user_cannot_update_group_curator(self) -> None:
        """
        Обычный пользователь не может обновить куратора группы.
        """

        with self.assertRaises(PermissionDenied):
            update_group_curator(
                actor=self.regular_user,
                group_curator=self.group_curator,
                data={
                    "notes": "Нет доступа",
                },
            )

    def test_remove_group_curator(self) -> None:
        """
        Сервис деактивирует куратора группы.
        """

        group_curator = remove_group_curator(
            actor=self.superadmin,
            group_curator=self.group_curator,
        )

        self.assertFalse(group_curator.is_active)
        self.assertFalse(group_curator.is_primary)

    def test_remove_inactive_group_curator_raises_error(self) -> None:
        """
        Повторная деактивация куратора возвращает ошибку.
        """

        self.group_curator.is_active = False
        self.group_curator.is_primary = False
        self.group_curator.save(
            update_fields=[
                "is_active",
                "is_primary",
            ]
        )

        with self.assertRaises(ValidationError):
            remove_group_curator(
                actor=self.superadmin,
                group_curator=self.group_curator,
            )

    def test_set_primary_group_curator(self) -> None:
        """
        Сервис делает куратора основным и снимает primary с другого.
        """

        second_curator = create_group_curator(
            group=self.group,
            teacher=self.second_teacher,
            is_primary=False,
            is_active=True,
        )

        group_curator = set_primary_group_curator(
            actor=self.superadmin,
            group_curator=second_curator,
        )

        self.group_curator.refresh_from_db()

        self.assertTrue(group_curator.is_primary)
        self.assertFalse(self.group_curator.is_primary)

    def test_cannot_set_inactive_group_curator_as_primary(self) -> None:
        """
        Неактивного куратора нельзя сделать основным.
        """

        self.group_curator.is_active = False
        self.group_curator.is_primary = False
        self.group_curator.save(
            update_fields=[
                "is_active",
                "is_primary",
            ]
        )

        with self.assertRaises(ValidationError):
            set_primary_group_curator(
                actor=self.superadmin,
                group_curator=self.group_curator,
            )