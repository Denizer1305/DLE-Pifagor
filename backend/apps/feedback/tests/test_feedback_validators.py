from __future__ import annotations

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from apps.feedback.validators import (
    validate_feedback_attachment,
    validate_feedback_attachments_count,
    validate_feedback_message,
    validate_feedback_name,
)


class FeedbackValidatorsTestCase(TestCase):
    def test_validate_feedback_name_accepts_correct_name(self) -> None:
        value = validate_feedback_name("Иван Иванов")

        self.assertEqual(value, "Иван Иванов")

    def test_validate_feedback_name_rejects_empty_name(self) -> None:
        with self.assertRaises(ValidationError):
            validate_feedback_name("")

    def test_validate_feedback_message_rejects_short_message(self) -> None:
        with self.assertRaises(ValidationError):
            validate_feedback_message("Коротко")

    def test_validate_feedback_message_rejects_profanity(self) -> None:
        with self.assertRaises(ValidationError):
            validate_feedback_message("Это сообщение содержит бля буду плохое слово.")

    def test_validate_feedback_attachments_count_rejects_more_than_five_files(self) -> None:
        files = [
            SimpleUploadedFile(
                f"file-{index}.pdf",
                b"test",
                content_type="application/pdf",
            )
            for index in range(6)
        ]

        with self.assertRaises(ValidationError):
            validate_feedback_attachments_count(files)

    def test_validate_feedback_attachment_accepts_pdf(self) -> None:
        file = SimpleUploadedFile(
            "request.pdf",
            b"test",
            content_type="application/pdf",
        )

        validate_feedback_attachment(file)

    def test_validate_feedback_attachment_rejects_exe(self) -> None:
        file = SimpleUploadedFile(
            "bad.exe",
            b"test",
            content_type="application/x-msdownload",
        )

        with self.assertRaises(ValidationError):
            validate_feedback_attachment(file)