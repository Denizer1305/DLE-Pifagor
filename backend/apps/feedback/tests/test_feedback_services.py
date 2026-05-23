from __future__ import annotations

from apps.feedback.models import FeedbackAttachment, FeedbackRequest
from apps.feedback.services import create_feedback_request
from django.contrib.auth import get_user_model
from django.core import mail
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory, TestCase

User = get_user_model()


class FeedbackServicesTestCase(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_create_feedback_request_saves_request_and_sends_email(self) -> None:
        request = self.factory.post("/api/v1/feedback/contact/")
        request.user = AnonymousUserMock()

        feedback_request = create_feedback_request(
            request=request,
            topic=FeedbackRequest.TopicChoices.PARTNERSHIP,
            full_name="Иван Иванов",
            email="ivan@example.com",
            phone="+79990000000",
            organization_name="Тестовая организация",
            subject="Подключение организации",
            message="Хотим обсудить подключение образовательной организации к ЦОС Пифагор.",
            is_personal_data_consent=True,
            page_url="http://localhost:5173/contacts",
            frontend_route="/contacts",
            files=[],
        )

        self.assertEqual(FeedbackRequest.objects.count(), 1)
        self.assertEqual(feedback_request.full_name, "Иван Иванов")
        self.assertEqual(feedback_request.status, FeedbackRequest.StatusChoices.NEW)
        self.assertTrue(feedback_request.admin_notification_sent)
        self.assertEqual(len(mail.outbox), 1)

    def test_create_feedback_request_saves_attachments(self) -> None:
        request = self.factory.post("/api/v1/feedback/contact/")
        request.user = AnonymousUserMock()

        file = SimpleUploadedFile(
            "document.pdf",
            b"test file content",
            content_type="application/pdf",
        )

        feedback_request = create_feedback_request(
            request=request,
            topic=FeedbackRequest.TopicChoices.QUESTION,
            full_name="Иван Иванов",
            email="ivan@example.com",
            message="Проверяем отправку обращения с вложением.",
            is_personal_data_consent=True,
            files=[file],
        )

        self.assertEqual(FeedbackAttachment.objects.count(), 1)

        attachment = feedback_request.attachments.first()

        self.assertIsNotNone(attachment)
        self.assertEqual(attachment.original_name, "document.pdf")
        self.assertEqual(attachment.kind, FeedbackAttachment.KindChoices.PDF)

    def test_create_feedback_request_links_authorized_user(self) -> None:
        user = User.objects.create_user(
            email="feedback-user@example.com",
            phone="+79991112233",
            password="StrongPassword123!",
            first_name="Иван",
            last_name="Иванов",
        )

        request = self.factory.post("/api/v1/feedback/contact/")
        request.user = user

        feedback_request = create_feedback_request(
            request=request,
            topic=FeedbackRequest.TopicChoices.QUESTION,
            full_name="Иван Иванов",
            email="feedback-user@example.com",
            message="Проверяем привязку авторизованного пользователя.",
            is_personal_data_consent=True,
            files=[],
        )

        self.assertEqual(feedback_request.user_id, user.id)


class AnonymousUserMock:
    is_authenticated = False
