"""
Сервисные функции безопасности пользовательских настроек.
"""

from __future__ import annotations


def build_security_sessions_payload(*, request) -> dict:
    """
    Собирает данные о текущей пользовательской сессии.

    Полноценная таблица устройств будет добавлена позже.
    Сейчас возвращается безопасная базовая информация о текущем запросе.
    """

    user_agent = request.META.get("HTTP_USER_AGENT", "")
    ip_address = get_client_ip(request)

    return {
        "items": [
            {
                "id": "current",
                "title": "Текущая сессия",
                "device": user_agent or "Неизвестное устройство",
                "ip_address": ip_address,
                "is_current": True,
                "last_activity": "",
            }
        ],
        "can_logout_all": True,
    }


def get_client_ip(request) -> str:
    """
    Возвращает IP-адрес клиента из запроса.
    """

    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR", "")
