from __future__ import annotations


def get_client_ip(request) -> str:
    """
    Получает IP-адрес клиента из request.

    Учитывает заголовок HTTP_X_FORWARDED_FOR, если приложение
    работает за прокси или балансировщиком.
    """

    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR", "")