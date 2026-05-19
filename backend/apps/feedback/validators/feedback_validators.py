from __future__ import annotations

import os
import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from apps.feedback.constants import (
    ALLOWED_FEEDBACK_ATTACHMENT_EXTENSIONS,
    ALLOWED_FEEDBACK_ATTACHMENT_MIME_TYPES,
    MAX_FEEDBACK_ATTACHMENTS_COUNT,
    MAX_FEEDBACK_ATTACHMENT_SIZE,
    PROFANITY_PATTERNS,
)


def normalize_feedback_text(value: str) -> str:
    return " ".join((value or "").strip().split())


def validate_no_profanity(value: str) -> str:
    normalized_value = (value or "").lower()

    for pattern in PROFANITY_PATTERNS:
        if re.search(pattern, normalized_value, flags=re.IGNORECASE):
            raise ValidationError(
                _("Текст содержит недопустимые выражения. Пожалуйста, переформулируйте сообщение.")
            )

    return value


def validate_feedback_name(value: str) -> str:
    value = normalize_feedback_text(value)

    if not value:
        raise ValidationError(_("Укажите имя."))

    if len(value) < 2:
        raise ValidationError(_("Имя должно содержать не менее 2 символов."))

    validate_no_profanity(value)

    return value


def validate_feedback_message(value: str) -> str:
    value = (value or "").strip()

    if not value:
        raise ValidationError(_("Сообщение не может быть пустым."))

    if len(value) < 10:
        raise ValidationError(_("Сообщение должно содержать не менее 10 символов."))

    if len(value) > 5000:
        raise ValidationError(_("Сообщение не должно превышать 5000 символов."))

    validate_no_profanity(value)

    return value


def validate_feedback_topic_text(value: str) -> str:
    value = normalize_feedback_text(value)

    if value:
        validate_no_profanity(value)

    return value


def validate_feedback_attachments_count(files) -> list:
    files = list(files or [])

    if len(files) > MAX_FEEDBACK_ATTACHMENTS_COUNT:
        raise ValidationError(
            _(f"Можно прикрепить не более {MAX_FEEDBACK_ATTACHMENTS_COUNT} файлов.")
        )

    return files


def validate_feedback_attachment(file_obj) -> None:
    filename = getattr(file_obj, "name", "") or ""
    content_type = getattr(file_obj, "content_type", "") or ""
    file_size = getattr(file_obj, "size", 0) or 0
    extension = os.path.splitext(filename)[1].lower()

    if extension not in ALLOWED_FEEDBACK_ATTACHMENT_EXTENSIONS:
        raise ValidationError(
            _("Поддерживаются только изображения, PDF, DOC и DOCX.")
        )

    if content_type and content_type not in ALLOWED_FEEDBACK_ATTACHMENT_MIME_TYPES:
        raise ValidationError(
            _("Тип файла не поддерживается.")
        )

    if file_size > MAX_FEEDBACK_ATTACHMENT_SIZE:
        raise ValidationError(
            _("Размер одного файла не должен превышать 5 МБ.")
        )