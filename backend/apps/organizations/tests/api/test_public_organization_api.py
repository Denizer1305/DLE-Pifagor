from __future__ import annotations

from apps.organizations.tests.factories import create_organization, create_teacher
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class PublicOrganizationApiTestCase(TestCase):
    """
    Тесты публичных API образовательных организаций.
    """

    def setUp(self) -> None:
        self.client = APIClient()

        self.default_organization = create_organization(
            name="ГАПОУ ВО «ВлГК им. Д.К. Советкина»",
            short_name="ВлГК им. Советкина",
            code="vlgk_sovetkina",
            slug="vlgk-sovetkina",
            city="Владимир",
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

        self.teacher = create_teacher(
            organization=self.default_organization,
            email="teacher@example.com",
            phone="+79990000010",
        )

    def test_public_organizations_list_returns_only_public_active(self) -> None:
        """
        Публичный список возвращает только активные публичные организации.
        """

        url = reverse("organizations:public-organizations-list")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        organization_ids = {item["id"] for item in payload}

        self.assertIn(self.default_organization.id, organization_ids)
        self.assertNotIn(self.hidden_organization.id, organization_ids)
        self.assertNotIn(self.inactive_organization.id, organization_ids)

    def test_default_public_organization_endpoint_returns_default(self) -> None:
        """
        Endpoint организации по умолчанию возвращает default_public организацию.
        """

        url = reverse("organizations:public-organizations-default")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["id"], self.default_organization.id)
        self.assertEqual(payload["code"], "vlgk_sovetkina")
        self.assertTrue(payload["is_default_public"])

    def test_default_public_organization_endpoint_returns_null_when_absent(
        self,
    ) -> None:
        """
        Если default_public организация не настроена, endpoint возвращает null.
        """

        self.default_organization.is_default_public = False
        self.default_organization.save(update_fields=["is_default_public"])

        url = reverse("organizations:public-organizations-default")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.json())

    def test_current_organization_requires_authentication(self) -> None:
        """
        Endpoint текущей организации требует авторизацию.
        """

        url = reverse("organizations:current-organization")

        response = self.client.get(url)

        self.assertIn(
            response.status_code,
            (
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ),
        )

    def test_current_organization_returns_authorized_user_organization(
        self,
    ) -> None:
        """
        Endpoint текущей организации возвращает организацию пользователя.
        """

        self.client.force_authenticate(user=self.teacher)

        url = reverse("organizations:current-organization")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["id"], self.default_organization.id)
        self.assertEqual(payload["short_name"], "ВлГК им. Советкина")
