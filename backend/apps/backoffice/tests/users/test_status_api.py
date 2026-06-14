from __future__ import annotations

from apps.backoffice.tests.users.base import BackofficeUsersApiTestCase
from apps.users.constants.lifecycle import UserStatus
from apps.users.models import UserAuditLog
from django.urls import reverse
from rest_framework import status


class BackofficeUsersStatusApiTests(BackofficeUsersApiTestCase):
    """
    Тесты status actions для backoffice/users.
    """

    def test_superadmin_can_block_user(self):
        """
        Суперадминистратор может заблокировать пользователя.
        """

        self.authenticate_as_superadmin()

        response = self.client.post(
            reverse(
                "backoffice_users:backoffice-users-block",
                kwargs={"pk": self.student.id},
            ),
            {
                "reason": "Нарушение правил платформы.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student.refresh_from_db()

        self.assertEqual(self.student.status, UserStatus.BLOCKED)
        self.assertFalse(self.student.is_active)
        self.assertTrue(UserAuditLog.objects.filter(target_user=self.student).exists())

    def test_superadmin_can_unblock_user(self):
        """
        Суперадминистратор может разблокировать пользователя.
        """

        self.student.status = UserStatus.BLOCKED
        self.student.is_active = False
        self.student.save(update_fields=["status", "is_active"])

        self.authenticate_as_superadmin()

        response = self.client.post(
            reverse(
                "backoffice_users:backoffice-users-unblock",
                kwargs={"pk": self.student.id},
            ),
            {
                "reason": "Проверка завершена.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student.refresh_from_db()

        self.assertEqual(self.student.status, UserStatus.ACTIVE)
        self.assertTrue(self.student.is_active)

    def test_superadmin_can_archive_user(self):
        """
        Суперадминистратор может архивировать пользователя.
        """

        self.authenticate_as_superadmin()

        response = self.client.post(
            reverse(
                "backoffice_users:backoffice-users-archive",
                kwargs={"pk": self.teacher.id},
            ),
            {
                "reason": "Пользователь больше не работает в организации.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.teacher.refresh_from_db()

        self.assertEqual(self.teacher.status, UserStatus.ARCHIVED)
        self.assertFalse(self.teacher.is_active)

    def test_superadmin_can_restore_archived_user(self):
        """
        Суперадминистратор может восстановить архивного пользователя.
        """

        self.teacher.status = UserStatus.ARCHIVED
        self.teacher.is_active = False
        self.teacher.save(update_fields=["status", "is_active"])

        self.authenticate_as_superadmin()

        response = self.client.post(
            reverse(
                "backoffice_users:backoffice-users-restore",
                kwargs={"pk": self.teacher.id},
            ),
            {
                "reason": "Пользователь возвращён.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.teacher.refresh_from_db()

        self.assertEqual(self.teacher.status, UserStatus.ACTIVE)
        self.assertTrue(self.teacher.is_active)

    def test_superadmin_cannot_block_self(self):
        """
        Администратор не может заблокировать самого себя.
        """

        self.authenticate_as_superadmin()

        response = self.client.post(
            reverse(
                "backoffice_users:backoffice-users-block",
                kwargs={"pk": self.superadmin.id},
            ),
            {
                "reason": "Нельзя заблокировать себя.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_regular_user_cannot_block_user(self):
        """
        Обычный пользователь не может менять статус пользователя.
        """

        self.authenticate_as_regular_user()

        response = self.client.post(
            reverse(
                "backoffice_users:backoffice-users-block",
                kwargs={"pk": self.student.id},
            ),
            {
                "reason": "Нет прав.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cannot_archive_scheduled_for_deletion_user(self):
        """
        Пользователя, запланированного к удалению, нельзя архивировать.
        """

        self.student.status = UserStatus.SCHEDULED_FOR_DELETION
        self.student.is_active = False
        self.student.scheduled_for_deletion_at = "2099-01-01T00:00:00Z"
        self.student.save(
            update_fields=[
                "status",
                "is_active",
                "scheduled_for_deletion_at",
            ]
        )

        self.authenticate_as_superadmin()

        response = self.client.post(
            reverse(
                "backoffice_users:backoffice-users-archive",
                kwargs={"pk": self.student.id},
            ),
            {
                "reason": "Нельзя архивировать.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
