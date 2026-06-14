from __future__ import annotations

import secrets
import uuid

CODE_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
"""Алфавит для человекочитаемых кодов без похожих символов."""


def generate_uuid_string() -> str:
    """
    Генерирует UUID в строковом формате.
    """

    return str(uuid.uuid4())


def generate_random_code(length: int = 8) -> str:
    """
    Генерирует случайный код из цифр и латинских букв.

    Используется для кодов приглашений, заявок и коротких токенов,
    которые должен читать человек.
    """

    return "".join(secrets.choice(CODE_ALPHABET) for _ in range(length))


def generate_numeric_code(length: int = 6) -> str:
    """
    Генерирует случайный числовой код.
    """

    return "".join(secrets.choice("0123456789") for _ in range(length))
