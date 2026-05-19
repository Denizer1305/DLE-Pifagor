from __future__ import annotations

from django.contrib.auth import get_user_model
from django.core import mail
from django.core.cache import cache
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

from apps.feedback.models import FeedbackAttachment, FeedbackRequest


User = get_user_model()


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)
class ContactFeedbackApiTestCase(TestCase):
    def setUp(self) -> None:
        cache.clear()

        self.client = APIClient()
        self.url = "/api/v1/feedback/contact/"

    def tearDown(self) -> None:
        cache.clear()

    def test_contact_feedback_creates_request(self) -> None:
        response = self.client.post(
            self.url,
            data={
                "topic": "partnership",
                "full_name": "Иван Иванов",
                "email": "ivan@example.com",
                "phone": "+79990000000",
                "organization_name": "Тестовая организация",
                "subject": "Подключение организации",
                "message": "Хотим обсудить подключение образовательной организации к платформе.",
                "is_personal_data_consent": "true",
                "page_url": "http://localhost:5173/contacts",
                "frontend_route": "/contacts",
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 201)

        payload = response.json()

        self.assertEqual(payload["status"], "new")
        self.assertEqual(payload["message"], "Спасибо! Ваше сообщение отправлено.")
        self.assertEqual(FeedbackRequest.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_contact_feedback_requires_consent(self) -> None:
        response = self.client.post(
            self.url,
            data={
                "topic": "question",
                "full_name": "Иван Иванов",
                "email": "ivan@example.com",
                "message": "Сообщение достаточной длины для проверки.",
                "is_personal_data_consent": "false",
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(FeedbackRequest.objects.count(), 0)

    def test_contact_feedback_rejects_profanity(self) -> None:
        response = self.client.post(
            self.url,
            data={
                "topic": "question",
                "full_name": "Иван Иванов",
                "email": "ivan@example.com",
                "message": "Тут есть бля запрещенное выражение.",
                "is_personal_data_consent": "true",
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(FeedbackRequest.objects.count(), 0)

    def test_contact_feedback_saves_attachment(self) -> None:
        file = SimpleUploadedFile(
            "request.pdf",
            b"test content",
            content_type="application/pdf",
        )

        response = self.client.post(
            self.url,
            data={
                "topic": "question",
                "full_name": "Иван Иванов",
                "email": "ivan@example.com",
                "message": "Отправляем сообщение с вложенным документом.",
                "is_personal_data_consent": "true",
                "attachments": [file],
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(FeedbackRequest.objects.count(), 1)
        self.assertEqual(FeedbackAttachment.objects.count(), 1)

    def test_contact_feedback_rejects_wrong_attachment_type(self) -> None:
        file = SimpleUploadedFile(
            "virus.exe",
            b"bad content",
            content_type="application/x-msdownload",
        )

        response = self.client.post(
            self.url,
            data={
                "topic": "question",
                "full_name": "Иван Иванов",
                "email": "ivan@example.com",
                "message": "Отправляем сообщение с плохим вложением.",
                "is_personal_data_consent": "true",
                "attachments": [file],
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(FeedbackRequest.objects.count(), 0)

    def test_contact_feedback_links_authorized_user(self) -> None:
        user = User.objects.create_user(
            email="authorized@example.com",
            phone="+79992223344",
            password="StrongPassword123!",
            first_name="Иван",
            last_name="Иванов",
        )

        self.client.force_authenticate(user=user)

        response = self.client.post(
            self.url,
            data={
                "topic": "technical_support",
                "full_name": "Иван Иванов",
                "email": "authorized@example.com",
                "message": "Нужно помочь с ошибкой в личном кабинете.",
                "is_personal_data_consent": "true",
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 201)

        feedback_request = FeedbackRequest.objects.first()

        self.assertIsNotNone(feedback_request)
        self.assertEqual(feedback_request.user_id, user.id)

    def test_contact_feedback_throttle_limits_requests(self) -> None:
        for index in range(3):
            response = self.client.post(
                self.url,
                data={
                    "topic": "question",
                    "full_name": f"Иван Иванов {index}",
                    "email": f"ivan{index}@example.com",
                    "message": "Проверяем ограничение количества запросов.",
                    "is_personal_data_consent": "true",
                },
                format="multipart",
            )

            self.assertEqual(response.status_code, 201)

        response = self.client.post(
            self.url,
            data={
                "topic": "question",
                "full_name": "Иван Иванов 4",
                "email": "ivan4@example.com",
                "message": "Четвёртый запрос должен быть ограничен.",
                "is_personal_data_consent": "true",
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, 429)
