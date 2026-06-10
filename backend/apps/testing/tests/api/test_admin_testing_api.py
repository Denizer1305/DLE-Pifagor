from __future__ import annotations

from unittest.mock import patch

from apps.testing.constants import TestAttemptStatus, TestStatus
from apps.testing.tests.factories import (
    create_attempt,
    create_choice_question_with_options,
    create_course,
    create_superadmin,
    create_teacher,
    create_test,
    extract_results,
)
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AdminTestingApiTestCase(APITestCase):
    """
    API-тесты административного пространства testing.
    """

    def setUp(self) -> None:
        """
        Подготавливает базовые данные.
        """

        self.superadmin = create_superadmin()
        self.course = create_course()
        self.teacher = create_teacher()
        self.exam = create_test(
            course=self.course,
            organization=self.course.organization,
            subject=self.course.subject,
            owner_teacher=self.teacher,
        )

    def test_superadmin_can_get_tests_list(self) -> None:
        """
        Суперадмин получает список тестов.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(reverse("testing_admin:testing-admin-tests-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        test_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(self.exam.id, test_ids)

    def test_superadmin_can_create_test(self) -> None:
        """
        Суперадмин создаёт тест.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse("testing_admin:testing-admin-tests-list"),
            {
                "title": "Новый тест",
                "description": "Описание теста.",
                "instructions": "Ответьте на вопросы.",
                "course_id": self.course.id,
                "organization_id": self.course.organization_id,
                "subject_id": self.course.subject_id,
                "owner_teacher_id": self.teacher.id,
                "max_attempts": 3,
                "max_score": 100,
                "passing_score": 50,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["title"], "Новый тест")
        self.assertEqual(response.json()["status"], TestStatus.DRAFT)

    def test_superadmin_can_publish_test(self) -> None:
        """
        Суперадмин публикует тест.
        """

        create_choice_question_with_options(test=self.exam)

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "testing_admin:testing-admin-tests-publish",
                args=[self.exam.id],
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], TestStatus.PUBLISHED)

        self.exam.refresh_from_db()
        self.assertEqual(self.exam.status, TestStatus.PUBLISHED)
        self.assertTrue(self.exam.is_active)

    def test_superadmin_can_archive_test(self) -> None:
        """
        Суперадмин архивирует тест.
        """

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "testing_admin:testing-admin-tests-archive",
                args=[self.exam.id],
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], TestStatus.ARCHIVED)

        self.exam.refresh_from_db()
        self.assertEqual(self.exam.status, TestStatus.ARCHIVED)
        self.assertFalse(self.exam.is_active)

    def test_superadmin_can_get_attempts_list(self) -> None:
        """
        Суперадмин получает список попыток.
        """

        attempt = create_attempt(test=self.exam)

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.get(reverse("testing_admin:testing-admin-attempts-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        attempt_ids = {item["id"] for item in extract_results(response.json())}

        self.assertIn(attempt.id, attempt_ids)

    @patch(
        "apps.testing.services.result.publication." "notify_guardian_about_test_result"
    )
    @patch(
        "apps.testing.services.result.publication." "notify_learner_about_test_result"
    )
    def test_superadmin_can_publish_attempt_result(
        self,
        notify_learner_mock,
        notify_guardian_mock,
    ) -> None:
        """
        Суперадмин публикует подтверждённый результат попытки.
        """

        attempt = create_attempt(
            test=self.exam,
            status=TestAttemptStatus.CONFIRMED,
            is_confirmed_by_teacher=True,
            final_score=80,
            final_grade=4,
        )

        self.client.force_authenticate(user=self.superadmin)

        response = self.client.post(
            reverse(
                "testing_admin:testing-admin-attempts-publish-result",
                args=[attempt.id],
            ),
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], TestAttemptStatus.PUBLISHED)
        self.assertTrue(response.json()["is_visible_to_learner"])
        self.assertTrue(response.json()["is_visible_to_guardian"])

        notify_learner_mock.assert_called_once()
        notify_guardian_mock.assert_called_once()
