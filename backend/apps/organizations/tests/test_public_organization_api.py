from __future__ import annotations

from apps.organizations.models import Organization
from apps.organizations.tests.factories import create_test_user
from apps.users.constants.lifecycle import ProfileStatus
from apps.users.models import TeacherProfile
from django.test import TestCase
from rest_framework.test import APIClient


class PublicOrganizationApiTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.default_organization = Organization.objects.create(
            name="ГАПОУ ВО «ВлГК им. Д.К. Советкина»",
            short_name="ВлГК им. Советкина",
            code="vlgk_sovetkina",
            slug="vlgk-sovetkina",
            city="Владимир",
            is_active=True,
            is_public=True,
            is_default_public=True,
        )

        self.hidden_organization = Organization.objects.create(
            name="Скрытая организация",
            short_name="Скрытая",
            code="hidden_org",
            slug="hidden-org",
            is_active=True,
            is_public=False,
            is_default_public=False,
        )

        self.teacher = create_test_user(
            email="teacher@example.com",
            phone="+79990000002",
            first_name="Иван",
            last_name="Иванов",
            middle_name="Иванович",
        )

        TeacherProfile.objects.create(
            user=self.teacher,
            organization=self.default_organization,
            status=ProfileStatus.VERIFIED,
            position="Преподаватель",
            is_public=True,
            show_on_teachers_page=True,
        )

    def test_public_organizations_list_returns_only_public_organizations(self) -> None:
        response = self.client.get("/api/v1/organizations/public/")

        self.assertEqual(response.status_code, 200)

        payload = response.json()

        self.assertEqual(len(payload), 1)
        self.assertEqual(payload[0]["id"], self.default_organization.id)
        self.assertEqual(payload[0]["short_name"], "ВлГК им. Советкина")

    def test_default_public_organization_endpoint_returns_default(self) -> None:
        response = self.client.get("/api/v1/organizations/public/default/")

        self.assertEqual(response.status_code, 200)

        payload = response.json()

        self.assertEqual(payload["id"], self.default_organization.id)
        self.assertEqual(payload["code"], "vlgk_sovetkina")
        self.assertTrue(payload["is_default_public"])

    def test_current_organization_requires_authentication(self) -> None:
        response = self.client.get("/api/v1/organizations/current/")

        self.assertIn(response.status_code, (401, 403))

    def test_current_organization_returns_authorized_user_organization(self) -> None:
        self.client.force_authenticate(user=self.teacher)

        response = self.client.get("/api/v1/organizations/current/")

        self.assertEqual(response.status_code, 200)

        payload = response.json()

        self.assertEqual(payload["id"], self.default_organization.id)
        self.assertEqual(payload["short_name"], "ВлГК им. Советкина")
