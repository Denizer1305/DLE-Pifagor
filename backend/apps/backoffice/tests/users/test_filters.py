from __future__ import annotations

from apps.backoffice.tests.users.base import BackofficeUsersApiTestCase
from django.urls import reverse
from rest_framework import status


class BackofficeUsersFilterApiTests(BackofficeUsersApiTestCase):
    """
    Тесты фильтрации списка пользователей backoffice.
    """

    def test_students_filter_returns_only_students(self):
        """
        role_group=students возвращает пользователей с ролью студента.
        """

        self.authenticate_as_superadmin()

        response = self.client.get(
            reverse("backoffice_users:backoffice-users-list"),
            {"role_group": "students"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        emails = {item["email"] for item in self.get_response_items(response)}

        self.assertIn(self.student.email, emails)
        self.assertNotIn(self.teacher.email, emails)
        self.assertNotIn(self.parent.email, emails)

    def test_teachers_filter_returns_only_teachers(self):
        """
        role_group=teachers возвращает преподавателей.
        """

        self.authenticate_as_superadmin()

        response = self.client.get(
            reverse("backoffice_users:backoffice-users-list"),
            {"role_group": "teachers"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        emails = {item["email"] for item in self.get_response_items(response)}

        self.assertIn(self.teacher.email, emails)
        self.assertNotIn(self.student.email, emails)
        self.assertNotIn(self.parent.email, emails)

    def test_parents_filter_returns_only_parents(self):
        """
        role_group=parents возвращает родителей.
        """

        self.authenticate_as_superadmin()

        response = self.client.get(
            reverse("backoffice_users:backoffice-users-list"),
            {"role_group": "parents"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        emails = {item["email"] for item in self.get_response_items(response)}

        self.assertIn(self.parent.email, emails)
        self.assertNotIn(self.student.email, emails)
        self.assertNotIn(self.teacher.email, emails)
