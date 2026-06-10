from __future__ import annotations

from apps.feedback.models import FeedbackRequest
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

User = get_user_model()


class FeedbackManagementApiTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.url = "/api/v1/feedback/admin/requests/"
        self.admin = User.objects.create_user(
            email="feedback-admin@example.com",
            phone="+79990000991",
            password="StrongPassword123!",
            first_name="Анна",
            last_name="Администратор",
            is_staff=True,
            is_superuser=True,
        )
        self.feedback_request = FeedbackRequest.objects.create(
            topic=FeedbackRequest.TopicChoices.QUESTION,
            full_name="Иван Иванов",
            email="ivan@example.com",
            message="Нужно уточнить порядок подключения к платформе.",
            is_personal_data_consent=True,
        )

    def test_admin_list_requires_authentication(self) -> None:
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 401)

    def test_admin_receives_feedback_requests_and_summary(self) -> None:
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["summary"]["new"], 1)
        self.assertEqual(response.data["items"][0]["id"], self.feedback_request.id)

    def test_admin_updates_feedback_status(self) -> None:
        self.client.force_authenticate(user=self.admin)
        url = f"{self.url}{self.feedback_request.id}/"

        response = self.client.patch(
            url,
            data={"status": FeedbackRequest.StatusChoices.IN_PROGRESS},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.feedback_request.refresh_from_db()
        self.assertEqual(
            self.feedback_request.status,
            FeedbackRequest.StatusChoices.IN_PROGRESS,
        )
