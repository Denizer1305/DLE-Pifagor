from __future__ import annotations

from apps.organizations.selectors import (
    get_admin_organizations_queryset_for_actor,
    get_default_public_organization,
    get_public_organizations_queryset,
    get_user_organization,
    resolve_public_teachers_organization,
)
from apps.organizations.tests.factories import (
    assign_user_role,
    create_organization,
    create_superadmin,
    create_teacher,
    create_test_user,
)
from apps.users.constants.roles import RoleCode
from django.test import TestCase


class OrganizationSelectorsTestCase(TestCase):
    """
    Тесты селекторов организаций.
    """

    def setUp(self) -> None:
        self.superadmin = create_superadmin(
            email="superadmin-org-selectors@example.com",
            phone="+79997000001",
        )
        self.regular_user = create_test_user(
            email="regular-org-selectors@example.com",
            phone="+79997000002",
        )

        self.default_organization = create_organization(
            name="Публичная организация",
            short_name="Публичная",
            code="public_org",
            slug="public-org",
            is_active=True,
            is_public=True,
            is_default_public=True,
        )
        self.hidden_organization = create_organization(
            name="Скрытая организация",
            short_name="Скрытая",
            code="hidden_org",
            slug="hidden-org",
            is_active=True,
            is_public=False,
            is_default_public=False,
        )
        self.inactive_organization = create_organization(
            name="Неактивная организация",
            short_name="Неактивная",
            code="inactive_org",
            slug="inactive-org",
            is_active=False,
            is_public=True,
            is_default_public=False,
        )

    def test_get_public_organizations_queryset_returns_only_active_public(self):
        """
        Публичный selector возвращает только активные публичные организации.
        """

        queryset = get_public_organizations_queryset()

        self.assertIn(self.default_organization, queryset)
        self.assertNotIn(self.hidden_organization, queryset)
        self.assertNotIn(self.inactive_organization, queryset)

    def test_get_default_public_organization_returns_default(self):
        """
        Selector возвращает default_public организацию.
        """

        organization = get_default_public_organization()

        self.assertEqual(organization, self.default_organization)

    def test_get_default_public_organization_can_be_absent(self):
        """
        Selector возвращает None, если default_public организация не настроена.
        """

        self.default_organization.is_default_public = False
        self.default_organization.save(update_fields=["is_default_public"])

        organization = get_default_public_organization()

        self.assertIsNone(organization)

    def test_get_user_organization_returns_teacher_profile_organization(self):
        """
        Selector возвращает организацию из профиля преподавателя.
        """

        teacher = create_teacher(
            organization=self.default_organization,
            email="teacher-org-selector@example.com",
            phone="+79997000003",
        )

        organization = get_user_organization(teacher)

        self.assertEqual(organization, self.default_organization)

    def test_resolve_public_teachers_organization_for_anonymous_user(self):
        """
        Для анонимного пользователя selector возвращает default_public.
        """

        organization = resolve_public_teachers_organization(None)

        self.assertEqual(organization, self.default_organization)

    def test_resolve_public_teachers_organization_for_authorized_user(self):
        """
        Для авторизованного преподавателя selector возвращает его организацию.
        """

        teacher_organization = create_organization(
            name="Организация преподавателя",
            short_name="Орг. преп.",
            code="teacher_public_org",
            slug="teacher-public-org",
            is_active=True,
            is_public=True,
            is_default_public=False,
        )
        teacher = create_teacher(
            organization=teacher_organization,
            email="teacher-own-org@example.com",
            phone="+79997000004",
        )

        organization = resolve_public_teachers_organization(teacher)

        self.assertEqual(organization, teacher_organization)

    def test_superadmin_sees_all_admin_organizations(self):
        """
        Суперадмин видит все организации в админке.
        """

        queryset = get_admin_organizations_queryset_for_actor(
            actor=self.superadmin,
        )

        self.assertIn(self.default_organization, queryset)
        self.assertIn(self.hidden_organization, queryset)
        self.assertIn(self.inactive_organization, queryset)

    def test_org_admin_sees_only_own_organization(self):
        """
        Администратор организации видит только свою организацию.
        """

        admin = create_test_user(
            email="org-admin-selector@example.com",
            phone="+79997000005",
        )
        assign_user_role(
            user=admin,
            role_code=RoleCode.ORG_ADMIN,
            organization=self.default_organization,
            assigned_by=self.superadmin,
        )

        queryset = get_admin_organizations_queryset_for_actor(actor=admin)

        self.assertIn(self.default_organization, queryset)
        self.assertNotIn(self.hidden_organization, queryset)
        self.assertNotIn(self.inactive_organization, queryset)

    def test_regular_user_sees_no_admin_organizations(self):
        """
        Обычный пользователь не видит организации в админке.
        """

        queryset = get_admin_organizations_queryset_for_actor(
            actor=self.regular_user,
        )

        self.assertEqual(queryset.count(), 0)