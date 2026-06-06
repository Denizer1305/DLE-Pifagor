from __future__ import annotations

from apps.organizations.selectors import (
    get_admin_departments_queryset_for_actor,
    get_departments_for_organization,
)
from apps.organizations.tests.factories import (
    assign_user_role,
    create_department,
    create_organization,
    create_superadmin,
    create_test_user,
)
from apps.users.constants.roles import RoleCode
from django.test import TestCase


class DepartmentSelectorsTestCase(TestCase):
    """
    Тесты селекторов отделений.
    """

    def setUp(self) -> None:
        self.superadmin = create_superadmin(
            email="superadmin-dept-selectors@example.com",
            phone="+79997100001",
        )
        self.regular_user = create_test_user(
            email="regular-dept-selectors@example.com",
            phone="+79997100002",
        )

        self.organization = create_organization(
            name="Организация отделений",
            short_name="Отделения",
            code="dept_selector_org",
            slug="dept-selector-org",
        )
        self.other_organization = create_organization(
            name="Другая организация отделений",
            short_name="Другая",
            code="other_dept_selector_org",
            slug="other-dept-selector-org",
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

    def test_get_departments_for_organization(self):
        """
        Selector возвращает отделения конкретной организации.
        """

        queryset = get_departments_for_organization(
            organization=self.organization,
        )

        self.assertIn(self.department, queryset)
        self.assertNotIn(self.other_department, queryset)

    def test_superadmin_sees_all_departments(self):
        """
        Суперадмин видит все отделения.
        """

        queryset = get_admin_departments_queryset_for_actor(
            actor=self.superadmin,
        )

        self.assertIn(self.department, queryset)
        self.assertIn(self.other_department, queryset)

    def test_org_admin_sees_departments_of_own_organization(self):
        """
        Администратор организации видит отделения своей организации.
        """

        admin = create_test_user(
            email="dept-org-admin@example.com",
            phone="+79997100003",
        )
        assign_user_role(
            user=admin,
            role_code=RoleCode.ORG_ADMIN,
            organization=self.organization,
            assigned_by=self.superadmin,
        )

        queryset = get_admin_departments_queryset_for_actor(actor=admin)

        self.assertIn(self.department, queryset)
        self.assertNotIn(self.other_department, queryset)

    def test_department_head_sees_own_department(self):
        """
        Заведующий отделением видит своё отделение.
        """

        head = create_test_user(
            email="department-head@example.com",
            phone="+79997100004",
        )
        assign_user_role(
            user=head,
            role_code=RoleCode.DEPARTMENT_HEAD,
            organization=self.organization,
            department=self.department,
            assigned_by=self.superadmin,
        )

        queryset = get_admin_departments_queryset_for_actor(actor=head)

        self.assertIn(self.department, queryset)
        self.assertNotIn(self.other_department, queryset)

    def test_regular_user_sees_no_departments(self):
        """
        Обычный пользователь не видит отделения в админке.
        """

        queryset = get_admin_departments_queryset_for_actor(
            actor=self.regular_user,
        )

        self.assertEqual(queryset.count(), 0)