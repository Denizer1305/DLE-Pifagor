from __future__ import annotations


def mask_email(email: str) -> str:
    """
    Маскирует email для безопасного отображения.

    Example:
        ivan@example.com -> i***@example.com
    """

    if not email or "@" not in email:
        return ""

    local_part, domain = email.split("@", 1)

    if len(local_part) <= 1:
        masked_local = "*"
    else:
        masked_local = f"{local_part[0]}***"

    return f"{masked_local}@{domain}"


def mask_phone(phone: str) -> str:
    """
    Маскирует номер телефона для безопасного отображения.
    """

    if not phone:
        return ""

    cleaned_phone = "".join(char for char in phone if char.isdigit() or char == "+")

    if len(cleaned_phone) <= 4:
        return "****"

    return f"{cleaned_phone[:2]}***{cleaned_phone[-2:]}"
