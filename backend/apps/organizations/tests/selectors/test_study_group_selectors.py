from __future__ import annotations

from apps.organizations.selectors import (
    get_admin_study_groups_queryset_for_actor,
    get_study_groups_for_department,
    get_study_groups_for_organization,
)
from apps.organizations.tests.factories import (
    assign_user_role,
    create_department,
    create_organization,
    create_study_group,
    create_superadmin,
    create_test_user,
)
from apps.users.constants.roles import RoleCode
from django.test import TestCase


class StudyGroupSelectorsTestCase(TestCase):
    """
    Тесты селекторов учебных групп.
    """

    def setUp(self) -> None:
        self.superadmin = create_superadmin(
            email="superadmin-group-selectors@example.com",
            phone="+79997200001",
        )
        self.regular_user = create_test_user(
            email="regular-group-selectors@example.com",
            phone="+79997200002",
        )

        self.organization = create_organization(
            name="Организация групп",
            short_name="Группы",
            code="group_selector_org",
            slug="group-selector-org",
        )
        self.other_organization = create_organization(
            name="Другая организация групп",
            short_name="Другая",
            code="other_group_selector_org",
            slug="other-group-selector-org",
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

    def test_get_study_groups_for_organization(self):
        """
        Selector возвращает группы организации.
        """

        queryset = get_study_groups_for_organization(
            organization=self.organization,
        )

        self.assertIn(self.group, queryset)
        self.assertNotIn(self.other_group, queryset)

    def test_get_study_groups_for_department(self):
        """
        Selector возвращает группы отделения.
        """

        queryset = get_study_groups_for_department(
            department=self.department,
        )

        self.assertIn(self.group, queryset)
        self.assertNotIn(self.other_group, queryset)

    def test_superadmin_sees_all_groups(self):
        """
        Суперадмин видит все группы.
        """

        queryset = get_admin_study_groups_queryset_for_actor(
            actor=self.superadmin,
        )

        self.assertIn(self.group, queryset)
        self.assertIn(self.other_group, queryset)

    def test_org_admin_sees_groups_of_own_organization(self):
        """
        Администратор организации видит группы своей организации.
        """

        admin = create_test_user(
            email="group-org-admin@example.com",
            phone="+79997200003",
        )
        assign_user_role(
            user=admin,
            role_code=RoleCode.ORG_ADMIN,
            organization=self.organization,
            assigned_by=self.superadmin,
        )

        queryset = get_admin_study_groups_queryset_for_actor(actor=admin)

        self.assertIn(self.group, queryset)
        self.assertNotIn(self.other_group, queryset)

    def test_department_head_sees_groups_of_own_department(self):
        """
        Заведующий отделением видит группы своего отделения.
        """

        head = create_test_user(
            email="group-department-head@example.com",
            phone="+79997200004",
        )
        assign_user_role(
            user=head,
            role_code=RoleCode.DEPARTMENT_HEAD,
            organization=self.organization,
            department=self.department,
            assigned_by=self.superadmin,
        )

        queryset = get_admin_study_groups_queryset_for_actor(actor=head)

        self.assertIn(self.group, queryset)
        self.assertNotIn(self.other_group, queryset)

    def test_curator_role_with_group_scope_sees_own_group(self):
        """
        Куратор с ролью на группу видит свою группу.
        """

        curator = create_test_user(
            email="group-curator-role@example.com",
            phone="+79997200005",
        )
        assign_user_role(
            user=curator,
            role_code=RoleCode.CURATOR,
            organization=self.organization,
            department=self.department,
            group=self.group,
            assigned_by=self.superadmin,
        )

        queryset = get_admin_study_groups_queryset_for_actor(actor=curator)

        self.assertIn(self.group, queryset)
        self.assertNotIn(self.other_group, queryset)

    def test_regular_user_sees_no_groups(self):
        """
        Обычный пользователь не видит группы в админке.
        """

        queryset = get_admin_study_groups_queryset_for_actor(
            actor=self.regular_user,
        )

        self.assertEqual(queryset.count(), 0)