from __future__ import annotations

from apps.organizations.selectors import (
    actor_is_group_curator,
    actor_is_primary_group_curator,
    get_admin_group_curators_queryset_for_actor,
    get_curated_group_ids_for_actor,
    get_curators_for_group,
    get_primary_curator_for_group,
)
from apps.organizations.tests.factories import (
    assign_user_role,
    create_department,
    create_group_curator,
    create_organization,
    create_study_group,
    create_superadmin,
    create_teacher,
    create_test_user,
)
from apps.users.constants.roles import RoleCode
from django.test import TestCase


class GroupCuratorSelectorsTestCase(TestCase):
    """
    Тесты селекторов кураторов групп.
    """

    def setUp(self) -> None:
        self.superadmin = create_superadmin(
            email="superadmin-curator-selectors@example.com",
            phone="+79997400001",
        )
        self.regular_user = create_test_user(
            email="regular-curator-selectors@example.com",
            phone="+79997400002",
        )

        self.organization = create_organization(
            name="Организация кураторов",
            short_name="Кураторы",
            code="curator_selector_org",
            slug="curator-selector-org",
        )
        self.other_organization = create_organization(
            name="Другая организация кураторов",
            short_name="Другая",
            code="other_curator_selector_org",
            slug="other-curator-selector-org",
        )

        self.department = create_department(
            organization=self.organization,
            name="ИТ-отделение",
            short_name="ИТ",
            code="it",
        )
        self.other_department = create_department(
            organization=self.other_organization,
            name="Экономическое отделение",
            short_name="Экономика",
            code="economics",
        )

        self.group = create_study_group(
            organization=self.organization,
            department=self.department,
            name="ИС-21",
            code="is_21",
        )
        self.other_group = create_study_group(
            organization=self.other_organization,
            department=self.other_department,
            name="ЭК-21",
            code="ek_21",
        )

        self.teacher = create_teacher(
            organization=self.organization,
            email="curator-selector@example.com",
            phone="+79997400003",
        )
        self.other_teacher = create_teacher(
            organization=self.other_organization,
            email="other-curator-selector@example.com",
            phone="+79997400004",
        )

        self.group_curator = create_group_curator(
            group=self.group,
            teacher=self.teacher,
            is_primary=True,
            is_active=True,
        )
        self.other_group_curator = create_group_curator(
            group=self.other_group,
            teacher=self.other_teacher,
            is_primary=True,
            is_active=True,
        )

    def test_get_curators_for_group(self):
        """
        Selector возвращает кураторов группы.
        """

        queryset = get_curators_for_group(group=self.group)

        self.assertIn(self.group_curator, queryset)
        self.assertNotIn(self.other_group_curator, queryset)

    def test_get_primary_curator_for_group(self):
        """
        Selector возвращает основного куратора группы.
        """

        curator = get_primary_curator_for_group(group=self.group)

        self.assertEqual(curator, self.group_curator)

    def test_actor_is_group_curator(self):
        """
        Selector определяет, является ли пользователь куратором группы.
        """

        self.assertTrue(
            actor_is_group_curator(
                actor=self.teacher,
                group=self.group,
            )
        )
        self.assertFalse(
            actor_is_group_curator(
                actor=self.teacher,
                group=self.other_group,
            )
        )

    def test_actor_is_primary_group_curator(self):
        """
        Selector определяет основного куратора группы.
        """

        self.assertTrue(
            actor_is_primary_group_curator(
                actor=self.teacher,
                group=self.group,
            )
        )
        self.assertFalse(
            actor_is_primary_group_curator(
                actor=self.other_teacher,
                group=self.group,
            )
        )

    def test_get_curated_group_ids_for_actor(self):
        """
        Selector возвращает ID курируемых групп пользователя.
        """

        group_ids = get_curated_group_ids_for_actor(actor=self.teacher)

        self.assertIn(self.group.id, group_ids)
        self.assertNotIn(self.other_group.id, group_ids)

    def test_superadmin_sees_all_group_curators(self):
        """
        Суперадмин видит всех кураторов групп.
        """

        queryset = get_admin_group_curators_queryset_for_actor(
            actor=self.superadmin,
        )

        self.assertIn(self.group_curator, queryset)
        self.assertIn(self.other_group_curator, queryset)

    def test_org_admin_sees_group_curators_of_own_organization(self):
        """
        Администратор организации видит кураторов групп своей организации.
        """

        admin = create_test_user(
            email="curator-org-admin-selector@example.com",
            phone="+79997400005",
        )
        assign_user_role(
            user=admin,
            role_code=RoleCode.ORG_ADMIN,
            organization=self.organization,
            assigned_by=self.superadmin,
        )

        queryset = get_admin_group_curators_queryset_for_actor(actor=admin)

        self.assertIn(self.group_curator, queryset)
        self.assertNotIn(self.other_group_curator, queryset)

    def test_department_head_sees_group_curators_of_own_department(self):
        """
        Заведующий отделением видит кураторов групп своего отделения.
        """

        head = create_test_user(
            email="curator-department-head-selector@example.com",
            phone="+79997400006",
        )
        assign_user_role(
            user=head,
            role_code=RoleCode.DEPARTMENT_HEAD,
            organization=self.organization,
            department=self.department,
            assigned_by=self.superadmin,
        )

        queryset = get_admin_group_curators_queryset_for_actor(actor=head)

        self.assertIn(self.group_curator, queryset)
        self.assertNotIn(self.other_group_curator, queryset)

    def test_regular_user_sees_no_group_curators(self):
        """
        Обычный пользователь не видит кураторов групп в админке.
        """

        queryset = get_admin_group_curators_queryset_for_actor(
            actor=self.regular_user,
        )

        self.assertEqual(queryset.count(), 0)