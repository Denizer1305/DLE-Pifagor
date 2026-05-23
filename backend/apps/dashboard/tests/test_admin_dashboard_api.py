from __future__ import annotations

from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.constants.roles import RoleCode
from apps.users.models import Role, UserRole
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

User = get_user_model()


class AdminDashboardSummaryApiTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = "/api/v1/dashboard/admin/summary/"

    def create_user(
        self,
        *,
        email: str,
        phone: str,
        is_superuser: bool = False,
        is_staff: bool = False,
    ):
        return User.objects.create_user(
            email=email,
            phone=phone,
            password="StrongPassword123!",
            first_name="Иван",
            last_name="Иванов",
            is_superuser=is_superuser,
            is_staff=is_staff,
        )

    def test_admin_summary_requires_authentication(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)

    def test_admin_summary_forbids_regular_user(self) -> None:
        user = self.create_user(
            email="regular@example.com",
            phone="+79990000001",
        )

        self.client.force_authenticate(user=user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_admin_summary_allows_superuser(self) -> None:
        user = self.create_user(
            email="admin@example.com",
            phone="+79990000002",
            is_superuser=True,
            is_staff=True,
        )

        self.client.force_authenticate(user=user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        payload = response.json()

        self.assertIn("profile", payload)
        self.assertIn("stats", payload)
        self.assertIn("calendar", payload)
        self.assertIn("recent_users", payload)
        self.assertIn("join_requests", payload)
        self.assertIn("feedback_requests", payload)
        self.assertIn("audit_events", payload)
        self.assertIn("system_health", payload)
        self.assertIn("quick_actions", payload)

        self.assertEqual(payload["profile"]["email"], "admin@example.com")
        self.assertTrue(len(payload["calendar"]["days"]) >= 35)

    def test_admin_summary_allows_superadmin_role(self) -> None:
        role, _ = Role.objects.get_or_create(
            code=RoleCode.SUPERADMIN,
            defaults={
                "label": "Суперадминистратор",
                "description": "Полный доступ к платформе.",
                "is_system": True,
                "is_active": True,
                "sort_order": 10,
            },
        )

        user = self.create_user(
            email="role-admin@example.com",
            phone="+79990000003",
        )

        UserRole.objects.create(
            user=user,
            role=role,
            status=UserRoleStatus.ACTIVE,
        )

        self.client.force_authenticate(user=user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_admin_summary_contains_user_stats(self) -> None:
        admin = self.create_user(
            email="admin2@example.com",
            phone="+79990000004",
            is_superuser=True,
            is_staff=True,
        )
        self.create_user(
            email="user1@example.com",
            phone="+79990000005",
        )
        self.create_user(
            email="user2@example.com",
            phone="+79990000006",
        )

        self.client.force_authenticate(user=admin)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

        payload = response.json()
        stats = {item["key"]: item for item in payload["stats"]}

        self.assertIn("users", stats)
        self.assertGreaterEqual(stats["users"]["value"], 3)
