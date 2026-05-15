import hashlib
import secrets
import uuid
from datetime import timedelta

from django.utils import timezone


def generate_uuid_string() -> str:
    """
    Генерирует UUID в строковом формате.

    Returns:
        str: UUID4 в виде строки.
    """

    return str(uuid.uuid4())


def generate_random_code(length: int = 8) -> str:
    """
    Генерирует случайный код из цифр и латинских букв.

    Args:
        length:
            Длина кода.

    Returns:
        str: Случайный код.
    """

    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"

    return "".join(secrets.choice(alphabet) for _ in range(length))


def generate_numeric_code(length: int = 6) -> str:
    """
    Генерирует случайный числовой код.

    Args:
        length:
            Длина кода.

    Returns:
        str: Числовой код.
    """

    return "".join(secrets.choice("0123456789") for _ in range(length))


def hash_value(value: str, *, salt: str = "") -> str:
    """
    Хеширует строковое значение через SHA-256.

    Используется для кодов приглашения и других значений,
    которые не нужно хранить в базе в открытом виде.

    Args:
        value:
            Исходное значение.
        salt:
            Дополнительная соль.

    Returns:
        str: SHA-256 хеш.
    """

    normalized_value = f"{salt}{value}".strip().lower()

    return hashlib.sha256(normalized_value.encode("utf-8")).hexdigest()


def now_plus_days(days: int):
    """
    Возвращает дату и время через указанное количество дней.

    Args:
        days:
            Количество дней.

    Returns:
        datetime: Текущее время + days.
    """

    return timezone.now() + timedelta(days=days)


def get_client_ip(request) -> str:
    """
    Получает IP-адрес клиента из request.

    Учитывает заголовок HTTP_X_FORWARDED_FOR, если приложение
    работает за прокси или балансировщиком.

    Args:
        request:
            Django/DRF request.

    Returns:
        str: IP-адрес клиента.
    """

    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR", "")


def mask_email(email: str) -> str:
    """
    Маскирует email для безопасного отображения.

    Example:
        ivan@example.com -> i***@example.com

    Args:
        email:
            Email пользователя.

    Returns:
        str: Замаскированный email.
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

    Args:
        phone:
            Номер телефона.

    Returns:
        str: Замаскированный номер телефона.
    """

    if not phone:
        return ""

    cleaned_phone = "".join(char for char in phone if char.isdigit() or char == "+")

    if len(cleaned_phone) <= 4:
        return "****"

    return f"{cleaned_phone[:2]}***{cleaned_phone[-2:]}"
