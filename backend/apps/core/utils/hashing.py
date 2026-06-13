from __future__ import annotations

import hashlib


def hash_value(value: str, *, salt: str = "") -> str:
    """
    Хеширует строковое значение через SHA-256.

    Используется для кодов приглашения и других значений,
    которые не нужно хранить в базе в открытом виде.
    """

    normalized_value = f"{salt}{value}".strip().lower()

    return hashlib.sha256(normalized_value.encode("utf-8")).hexdigest()