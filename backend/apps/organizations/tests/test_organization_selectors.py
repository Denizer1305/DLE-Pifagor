from __future__ import annotations

from apps.organizations.models import Organization
from apps.organizations.selectors import (
    get_default_public_organization,
    get_user_organization,
    resolve_public_teachers_organization,
)
from apps.organizations.tests.factories import create_test_user
from apps.users.constants.lifecycle import ProfileStatus
from apps.users.models import TeacherProfile
from django.test import TestCase


class OrganizationSelectorsTestCase(TestCase):
    def setUp(self) -> None:
        self.default_organization = Organization.objects.create(
            name="ГАПОУ ВО «ВлГК им. Д.К. Советкина»",
            short_name="ВлГК им. Советкина",
            code="vlgk_sovetkina",
            slug="vlgk-sovetkina",
            is_active=True,
            is_public=True,
            is_default_public=True,
        )

        self.other_organization = Organization.objects.create(
            name="Тестовая образовательная организация",
            short_name="Тестовая организация",
            code="test_organization",
            slug="test-organization",
            is_active=True,
            is_public=True,
            is_default_public=False,
        )

        self.teacher = create_test_user(
            email="teacher@example.com",
            phone="+79990000001",
            first_name="Иван",
            last_name="Иванов",
            middle_name="Иванович",
        )

        self.teacher_profile = TeacherProfile.objects.create(
            user=self.teacher,
            organization=self.other_organization,
            status=ProfileStatus.VERIFIED,
            position="Преподаватель математики",
            is_public=True,
            show_on_teachers_page=True,
        )

    def test_get_default_public_organization_returns_default(self) -> None:
        organization = get_default_public_organization()

        self.assertIsNotNone(organization)
        self.assertEqual(organization.id, self.default_organization.id)

    def test_get_user_organization_returns_teacher_organization(self) -> None:
        organization = get_user_organization(self.teacher)

        self.assertIsNotNone(organization)
        self.assertEqual(organization.id, self.other_organization.id)

    def test_resolve_public_teachers_organization_for_authorized_user(self) -> None:
        organization = resolve_public_teachers_organization(self.teacher)

        self.assertIsNotNone(organization)
        self.assertEqual(organization.id, self.other_organization.id)

    def test_resolve_public_teachers_organization_for_anonymous_user(self) -> None:
        organization = resolve_public_teachers_organization(None)

        self.assertIsNotNone(organization)
        self.assertEqual(organization.id, self.default_organization.id)

    def test_default_public_organization_can_be_absent(self) -> None:
        self.default_organization.is_default_public = False
        self.default_organization.save(update_fields=["is_default_public"])

        organization = get_default_public_organization()

        self.assertIsNone(organization)
