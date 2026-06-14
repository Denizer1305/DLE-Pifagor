from __future__ import annotations

from apps.backoffice.constants import BackofficeUserBulkAction
from apps.backoffice.tests.users.base import BackofficeUsersApiTestCase
from apps.users.constants.lifecycle import UserRoleStatus, UserStatus
from apps.users.models import UserRole
from django.urls import reverse
from rest_framework import status


class BackofficeUsersBulkApiTests(BackofficeUsersApiTestCase):
    """
    Тесты массовых операций backoffice/users.
    """

    def test_superadmin_can_bulk_block_users(self):
        """
        Суперадминистратор может массово заблокировать пользователей.
        """

        self.authenticate_as_superadmin()

        response = self.client.post(
            reverse("backoffice_users:backoffice-users-bulk"),
            {
                "action": BackofficeUserBulkAction.BLOCK,
                "user_ids": [
                    self.student.id,
                    self.teacher.id,
                ],
                "reason": "Тестовая массовая блокировка.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_count"], 2)
        self.assertEqual(response.data["success_count"], 2)
        self.assertEqual(response.data["failed_count"], 0)

        self.student.refresh_from_db()
        self.teacher.refresh_from_db()

        self.assertEqual(self.student.status, UserStatus.BLOCKED)
        self.assertEqual(self.teacher.status, UserStatus.BLOCKED)

    def test_superadmin_can_bulk_restore_users(self):
        """
        Суперадминистратор может массово восстановить пользователей.
        """

        for user in [self.student, self.teacher]:
            user.status = UserStatus.BLOCKED
            user.is_active = False
            user.save(update_fields=["status", "is_active"])

        self.authenticate_as_superadmin()

        response = self.client.post(
            reverse("backoffice_users:backoffice-users-bulk"),
            {
                "action": BackofficeUserBulkAction.RESTORE,
                "user_ids": [
                    self.student.id,
                    self.teacher.id,
                ],
                "reason": "Тестовое массовое восстановление.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["success_count"], 2)

        self.student.refresh_from_db()
        self.teacher.refresh_from_db()

        self.assertEqual(self.student.status, UserStatus.ACTIVE)
        self.assertEqual(self.teacher.status, UserStatus.ACTIVE)
        self.assertTrue(self.student.is_active)
        self.assertTrue(self.teacher.is_active)

    def test_superadmin_can_bulk_change_roles(self):
        """
        Суперадминистратор может массово назначить роль пользователям.
        """

        self.authenticate_as_superadmin()

        response = self.client.post(
            reverse("backoffice_users:backoffice-users-bulk"),
            {
                "action": BackofficeUserBulkAction.CHANGE_ROLES,
                "user_ids": [
                    self.student.id,
                    self.teacher.id,
                ],
                "role_payload": {
                    "assigned_roles": [
                        {
                            "role_id": self.guardian_role.id,
                        }
                    ],
                },
                "reason": "Тестовое массовое назначение роли.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_count"], 2)
        self.assertEqual(response.data["success_count"], 2)
        self.assertEqual(response.data["failed_count"], 0)

        self.assertTrue(
            UserRole.objects.filter(
                user=self.student,
                role=self.guardian_role,
                status=UserRoleStatus.ACTIVE,
            ).exists()
        )
        self.assertTrue(
            UserRole.objects.filter(
                user=self.teacher,
                role=self.guardian_role,
                status=UserRoleStatus.ACTIVE,
            ).exists()
        )

    def test_bulk_change_roles_requires_role_payload(self):
        """
        Bulk change_roles требует role_payload.
        """

        self.authenticate_as_superadmin()

        response = self.client.post(
            reverse("backoffice_users:backoffice-users-bulk"),
            {
                "action": BackofficeUserBulkAction.CHANGE_ROLES,
                "user_ids": [
                    self.student.id,
                ],
                "reason": "Нет role_payload.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_regular_user_cannot_execute_bulk_action(self):
        """
        Обычный пользователь не может выполнять bulk-операции.
        """

        self.authenticate_as_regular_user()

        response = self.client.post(
            reverse("backoffice_users:backoffice-users-bulk"),
            {
                "action": BackofficeUserBulkAction.BLOCK,
                "user_ids": [
                    self.student.id,
                    self.teacher.id,
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_bulk_action_returns_failed_item_for_unknown_user(self):
        """
        Ошибка одного пользователя не ломает всю bulk-операцию.
        """

        self.authenticate_as_superadmin()

        response = self.client.post(
            reverse("backoffice_users:backoffice-users-bulk"),
            {
                "action": BackofficeUserBulkAction.BLOCK,
                "user_ids": [
                    self.student.id,
                    999999,
                ],
                "reason": "Один пользователь не существует.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_count"], 2)
        self.assertEqual(response.data["success_count"], 1)
        self.assertEqual(response.data["failed_count"], 1)
