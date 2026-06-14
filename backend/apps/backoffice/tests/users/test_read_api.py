from __future__ import annotations

from apps.backoffice.tests.users.base import BackofficeUsersApiTestCase
from apps.users.constants.audit import UserAuditAction
from apps.users.constants.roles import RoleCode
from apps.users.models import UserAuditLog
from django.urls import reverse
from rest_framework import status


class BackofficeUsersReadApiTests(BackofficeUsersApiTestCase):
    """
    Тесты read-endpoints backoffice/users.
    """

    def test_superadmin_can_get_user_detail(self):
        """
        Суперадминистратор может открыть карточку пользователя.
        """

        self.authenticate_as_superadmin()

        response = self.client.get(
            reverse(
                "backoffice_users:backoffice-users-detail",
                kwargs={"pk": self.student.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.student.id)
        self.assertEqual(response.data["email"], self.student.email)
        self.assertIn("user_roles", response.data)
        self.assertIn("audit_logs", response.data)

    def test_detail_returns_404_for_unknown_user(self):
        """
        Неизвестный пользователь возвращает 404.
        """

        self.authenticate_as_superadmin()

        response = self.client.get(
            reverse(
                "backoffice_users:backoffice-users-detail",
                kwargs={"pk": 999999},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_available_roles_returns_active_roles(self):
        """
        Endpoint available-roles возвращает активные роли.
        """

        self.authenticate_as_superadmin()

        response = self.client.get(
            reverse("backoffice_users:backoffice-users-available-roles")
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        items = self.get_response_items(response)
        role_codes = {item["code"] for item in items}

        self.assertIn(RoleCode.LEARNER, role_codes)
        self.assertIn(RoleCode.TEACHER, role_codes)
        self.assertIn(RoleCode.GUARDIAN, role_codes)

    def test_audit_logs_endpoint_returns_user_history(self):
        """
        Endpoint audit-logs возвращает историю действий по пользователю.
        """

        UserAuditLog.objects.create(
            actor=self.superadmin,
            target_user=self.student,
            action=UserAuditAction.PROFILE_UPDATED,
            actor_type="admin",
            message="Тестовая запись аудита.",
            metadata={"source": "test"},
        )

        self.authenticate_as_superadmin()

        response = self.client.get(
            reverse(
                "backoffice_users:backoffice-users-audit-logs",
                kwargs={"pk": self.student.id},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(self.get_response_items(response)), 1)
