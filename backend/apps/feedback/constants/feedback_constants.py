from __future__ import annotations

CONTACT_FEEDBACK_ADMIN_EMAIL = "Pifagor-Platform33@yandex.ru"

MAX_FEEDBACK_ATTACHMENTS_COUNT = 5
MAX_FEEDBACK_ATTACHMENT_SIZE = 5 * 1024 * 1024

ALLOWED_FEEDBACK_ATTACHMENT_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".pdf",
    ".doc",
    ".docx",
}

ALLOWED_FEEDBACK_ATTACHMENT_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

PROFANITY_PATTERNS = (
    "хуй",
    "хуе",
    "хуё",
    "пизд",
    "еба",
    "ебл",
    "ёба",
    "бля",
    "бляд",
    "сука",
    "мраз",
)
