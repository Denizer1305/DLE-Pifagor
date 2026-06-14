from __future__ import annotations

from apps.backoffice.tests.users.base import BackofficeUsersApiTestCase
from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.models import UserAuditLog, UserRole
from django.urls import reverse
from rest_framework import status


class BackofficeUsersRolesApiTests(BackofficeUsersApiTestCase):
    """
    Тесты управления ролями пользователя через backoffice/users.
    """

    def test_superadmin_can_assign_role_to_user(self):
        """
        Суперадминистратор может назначить роль пользователю.
        """

        self.authenticate_as_superadmin()

        response = self.client.post(
            reverse(
                "backoffice_users:backoffice-users-change-roles",
                kwargs={"pk": self.student.id},
            ),
            {
                "assigned_roles": [
                    {
                        "role_id": self.teacher_role.id,
                    }
                ],
                "reason": "Тестовое назначение роли.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(
            UserRole.objects.filter(
                user=self.student,
                role=self.teacher_role,
                status=UserRoleStatus.ACTIVE,
            ).exists()
        )
        self.assertTrue(UserAuditLog.objects.filter(target_user=self.student).exists())

    def test_superadmin_can_revoke_user_role(self):
        """
        Суперадминистратор может отозвать роль пользователя.
        """

        user_role = UserRole.objects.get(
            user=self.student,
            role=self.learner_role,
        )

        self.authenticate_as_superadmin()

        response = self.client.post(
            reverse(
                "backoffice_users:backoffice-users-change-roles",
                kwargs={"pk": self.student.id},
            ),
            {
                "revoked_user_role_ids": [
                    user_role.id,
                ],
                "reason": "Тестовый отзыв роли.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_role.refresh_from_db()

        self.assertEqual(user_role.status, UserRoleStatus.REVOKED)
        self.assertEqual(user_role.revoked_by, self.superadmin)
        self.assertIsNotNone(user_role.revoked_at)

    def test_change_roles_requires_payload(self):
        """
        Нельзя вызвать change-roles без назначения или отзыва ролей.
        """

        self.authenticate_as_superadmin()

        response = self.client.post(
            reverse(
                "backoffice_users:backoffice-users-change-roles",
                kwargs={"pk": self.student.id},
            ),
            {
                "reason": "Пустой payload.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_regular_user_cannot_change_roles(self):
        """
        Обычный пользователь не может менять роли.
        """

        self.authenticate_as_regular_user()

        response = self.client.post(
            reverse(
                "backoffice_users:backoffice-users-change-roles",
                kwargs={"pk": self.student.id},
            ),
            {
                "assigned_roles": [
                    {
                        "role_id": self.teacher_role.id,
                    }
                ],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superadmin_cannot_change_own_roles(self):
        """
        Администратор не может менять собственные роли через backoffice.
        """

        self.authenticate_as_superadmin()

        response = self.client.post(
            reverse(
                "backoffice_users:backoffice-users-change-roles",
                kwargs={"pk": self.superadmin.id},
            ),
            {
                "assigned_roles": [
                    {
                        "role_id": self.learner_role.id,
                    }
                ],
                "reason": "Нельзя менять собственные роли.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
