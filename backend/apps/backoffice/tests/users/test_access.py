from __future__ import annotations

from apps.backoffice.tests.users.base import BackofficeUsersApiTestCase
from django.urls import reverse
from rest_framework import status


class BackofficeUsersAccessApiTests(BackofficeUsersApiTestCase):
    """
    Тесты доступа к backoffice/users.
    """

    def test_superadmin_can_get_users_list(self):
        """
        Суперадминистратор может открыть список пользователей.
        """

        self.authenticate_as_superadmin()

        response = self.client.get(reverse("backoffice_users:backoffice-users-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(self.get_response_total_count(response), 4)

    def test_regular_user_cannot_get_users_list(self):
        """
        Обычный пользователь не может открыть backoffice/users.
        """

        self.authenticate_as_regular_user()

        response = self.client.get(reverse("backoffice_users:backoffice-users-list"))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_user_cannot_get_users_list(self):
        """
        Анонимный пользователь не может открыть backoffice/users.
        """

        response = self.client.get(reverse("backoffice_users:backoffice-users-list"))

        self.assertIn(
            response.status_code,
            [
                status.HTTP_401_UNAUTHORIZED,
                status.HTTP_403_FORBIDDEN,
            ],
        )

    def test_backoffice_user_routes_are_registered(self):
        """
        Основные маршруты backoffice/users зарегистрированы.
        """

        routes = [
            reverse("backoffice_users:backoffice-users-list"),
            reverse(
                "backoffice_users:backoffice-users-detail",
                kwargs={"pk": self.student.id},
            ),
            reverse(
                "backoffice_users:backoffice-users-block",
                kwargs={"pk": self.student.id},
            ),
            reverse(
                "backoffice_users:backoffice-users-change-roles",
                kwargs={"pk": self.student.id},
            ),
            reverse("backoffice_users:backoffice-users-bulk"),
            reverse("backoffice_users:backoffice-users-available-roles"),
        ]

        self.assertTrue(all(routes))
