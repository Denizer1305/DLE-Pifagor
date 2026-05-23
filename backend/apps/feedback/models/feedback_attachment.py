from __future__ import annotations

import os
import uuid

from apps.core.models import TimeStampedModel
from apps.feedback.validators import validate_feedback_attachment
from django.db import models
from django.utils.translation import gettext_lazy as _


def feedback_attachment_upload_to(instance, filename: str) -> str:
    extension = os.path.splitext(filename)[1].lower()
    return f"feedback/attachments/{uuid.uuid4().hex}{extension}"


class FeedbackAttachment(TimeStampedModel):
    class KindChoices(models.TextChoices):
        IMAGE = "image", _("Изображение")
        PDF = "pdf", _("PDF")
        DOCUMENT = "document", _("Документ")
        OTHER = "other", _("Другое")

    feedback_request = models.ForeignKey(
        "feedback.FeedbackRequest",
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name=_("Обращение"),
    )
    file = models.FileField(
        _("Файл"),
        upload_to=feedback_attachment_upload_to,
        validators=[validate_feedback_attachment],
    )
    original_name = models.CharField(
        _("Оригинальное имя файла"),
        max_length=255,
        blank=True,
    )
    mime_type = models.CharField(
        _("MIME-тип"),
        max_length=120,
        blank=True,
    )
    file_size = models.PositiveIntegerField(
        _("Размер файла"),
        default=0,
    )
    kind = models.CharField(
        _("Тип файла"),
        max_length=32,
        choices=KindChoices.choices,
        default=KindChoices.OTHER,
    )

    class Meta:
        db_table = "feedback_attachment"
        verbose_name = _("Вложение обращения")
        verbose_name_plural = _("Вложения обращений")
        ordering = ("created_at",)
        indexes = [
            models.Index(
                fields=["feedback_request", "created_at"],
                name="fb_attach_req_idx",
            ),
            models.Index(
                fields=["kind", "created_at"],
                name="fb_attach_kind_idx",
            ),
        ]

    def save(self, *args, **kwargs) -> None:
        if self.file:
            self.original_name = self.original_name or os.path.basename(self.file.name)
            self.mime_type = getattr(self.file, "content_type", "") or ""
            self.file_size = getattr(self.file, "size", 0) or 0

            extension = os.path.splitext(self.original_name)[1].lower()

            if extension in {".jpg", ".jpeg", ".png", ".webp"}:
                self.kind = self.KindChoices.IMAGE
            elif extension == ".pdf":
                self.kind = self.KindChoices.PDF
            elif extension in {".doc", ".docx"}:
                self.kind = self.KindChoices.DOCUMENT
            else:
                self.kind = self.KindChoices.OTHER

        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.original_name or f"Вложение #{self.pk}"
