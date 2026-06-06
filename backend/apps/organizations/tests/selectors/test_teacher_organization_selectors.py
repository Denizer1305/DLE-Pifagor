from __future__ import annotations

from apps.organizations.selectors import (
    get_admin_teacher_organizations_queryset_for_actor,
    get_primary_teacher_organization,
    get_teacher_organizations_for_teacher,
)
from apps.organizations.tests.factories import (
    assign_user_role,
    create_organization,
    create_superadmin,
    create_teacher,
    create_teacher_organization,
    create_test_user,
)
from apps.users.constants.roles import RoleCode
from django.test import TestCase


class TeacherOrganizationSelectorsTestCase(TestCase):
    """
    Тесты селекторов связей преподавателей с организациями.
    """

    def setUp(self) -> None:
        self.superadmin = create_superadmin(
            email="superadmin-teacher-org-selectors@example.com",
            phone="+79997300001",
        )
        self.regular_user = create_test_user(
            email="regular-teacher-org-selectors@example.com",
            phone="+79997300002",
        )

        self.organization = create_organization(
            name="Организация преподавателей",
            short_name="Преподаватели",
            code="teacher_org_selector",
            slug="teacher-org-selector",
        )
        self.other_organization = create_organization(
            name="Другая организация преподавателей",
            short_name="Другая",
            code="other_teacher_org_selector",
            slug="other-teacher-org-selector",
        )

        self.teacher = create_teacher(
            organization=self.organization,
            email="teacher-selector@example.com",
            phone="+79997300003",
        )

        self.teacher_organization = create_teacher_organization(
            teacher=self.teacher,
            organization=self.organization,
            is_primary=True,
            is_active=True,
        )
        self.other_teacher_organization = create_teacher_organization(
            teacher=self.teacher,
            organization=self.other_organization,
            is_primary=False,
            is_active=True,
        )

    def test_get_teacher_organizations_for_teacher(self):
        """
        Selector возвращает организации преподавателя.
        """

        queryset = get_teacher_organizations_for_teacher(
            teacher=self.teacher,
        )

        self.assertIn(self.teacher_organization, queryset)
        self.assertIn(self.other_teacher_organization, queryset)

    def test_get_primary_teacher_organization(self):
        """
        Selector возвращает основную организацию преподавателя.
        """

        teacher_organization = get_primary_teacher_organization(
            teacher=self.teacher,
        )

        self.assertEqual(teacher_organization, self.teacher_organization)

    def test_superadmin_sees_all_teacher_organizations(self):
        """
        Суперадмин видит все связи преподавателей.
        """

        queryset = get_admin_teacher_organizations_queryset_for_actor(
            actor=self.superadmin,
        )

        self.assertIn(self.teacher_organization, queryset)
        self.assertIn(self.other_teacher_organization, queryset)

    def test_org_admin_sees_teacher_organizations_of_own_organization(self):
        """
        Администратор организации видит связи своей организации.
        """

        admin = create_test_user(
            email="teacher-org-admin-selector@example.com",
            phone="+79997300004",
        )
        assign_user_role(
            user=admin,
            role_code=RoleCode.ORG_ADMIN,
            organization=self.organization,
            assigned_by=self.superadmin,
        )

        queryset = get_admin_teacher_organizations_queryset_for_actor(
            actor=admin,
        )

        self.assertIn(self.teacher_organization, queryset)
        self.assertNotIn(self.other_teacher_organization, queryset)

    def test_regular_user_sees_no_teacher_organizations(self):
        """
        Обычный пользователь не видит связи преподавателей в админке.
        """

        queryset = get_admin_teacher_organizations_queryset_for_actor(
            actor=self.regular_user,
        )

        self.assertEqual(queryset.count(), 0)