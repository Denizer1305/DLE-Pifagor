from __future__ import annotations

from apps.backoffice.tests.users.base import BackofficeUsersApiTestCase
from apps.users.constants.lifecycle import UserStatus
from apps.users.models import UserAuditLog
from django.urls import reverse
from rest_framework import status


class BackofficeUsersMutationApiTests(BackofficeUsersApiTestCase):
    """
    Тесты изменения базовых данных пользователя через backoffice.
    """

    def test_superadmin_can_update_user_base_fields(self):
        """
        Суперадминистратор может обновить базовые поля пользователя.
        """

        self.authenticate_as_superadmin()

        response = self.client.patch(
            reverse(
                "backoffice_users:backoffice-users-detail",
                kwargs={"pk": self.student.id},
            ),
            {
                "first_name": "Алексей",
                "last_name": "Обновлённый",
                "reason": "Исправление данных профиля.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student.refresh_from_db()

        self.assertEqual(self.student.first_name, "Алексей")
        self.assertEqual(self.student.last_name, "Обновлённый")
        self.assertEqual(self.student.status, UserStatus.ACTIVE)
        self.assertTrue(UserAuditLog.objects.filter(target_user=self.student).exists())

    def test_regular_user_cannot_update_user(self):
        """
        Обычный пользователь не может редактировать пользователя.
        """

        self.authenticate_as_regular_user()

        response = self.client.patch(
            reverse(
                "backoffice_users:backoffice-users-detail",
                kwargs={"pk": self.student.id},
            ),
            {
                "first_name": "Ошибка",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_requires_payload(self):
        """
        Пустой update-payload возвращает 400.
        """

        self.authenticate_as_superadmin()

        response = self.client.patch(
            reverse(
                "backoffice_users:backoffice-users-detail",
                kwargs={"pk": self.student.id},
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_with_stale_expected_updated_at_returns_400(self):
        """
        Несовпадение expected_updated_at возвращает ошибку optimistic locking.
        """

        self.authenticate_as_superadmin()

        response = self.client.patch(
            reverse(
                "backoffice_users:backoffice-users-detail",
                kwargs={"pk": self.student.id},
            ),
            {
                "first_name": "Алексей",
                "expected_updated_at": "2000-01-01T00:00:00Z",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_superadmin_can_schedule_user_deletion(self):
        """
        DELETE не удаляет пользователя физически, а планирует удаление.
        """

        self.authenticate_as_superadmin()

        response = self.client.delete(
            reverse(
                "backoffice_users:backoffice-users-detail",
                kwargs={"pk": self.student.id},
            ),
            {
                "reason": "Тестовое планирование удаления.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.student.refresh_from_db()

        self.assertEqual(self.student.status, UserStatus.SCHEDULED_FOR_DELETION)
        self.assertFalse(self.student.is_active)
        self.assertIsNotNone(self.student.scheduled_for_deletion_at)

    def test_superadmin_cannot_schedule_self_deletion(self):
        """
        Администратор не может запланировать удаление самого себя.
        """

        self.authenticate_as_superadmin()

        response = self.client.delete(
            reverse(
                "backoffice_users:backoffice-users-detail",
                kwargs={"pk": self.superadmin.id},
            ),
            {
                "reason": "Нельзя удалить себя.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
