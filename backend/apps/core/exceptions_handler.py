"""
Единый обработчик исключений DRF.

Нужен для того, чтобы API возвращал ошибки в одном формате:

{
    "error": {
        "code": "...",
        "message": "...",
        "details": {}
    }
}
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.views import exception_handler

from core.exceptions import ApplicationError
from core.responses import error_response


def custom_exception_handler(exc, context):
    """
    Обрабатывает исключения DRF и приложения.

    Args:
        exc:
            Исключение.
        context:
            Контекст DRF.

    Returns:
        Response: Ответ с ошибкой в едином формате.
    """

    if isinstance(exc, ApplicationError):
        return error_response(
            code=exc.code,
            message=exc.message,
            details=exc.details,
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    response = exception_handler(exc, context)

    if response is None:
        return None

    error_code = getattr(exc, "default_code", "api_error")
    error_message = _extract_error_message(response.data)

    response.data = {
        "error": {
            "code": str(error_code),
            "message": error_message,
            "details": response.data,
        }
    }

    return response


def _extract_error_message(data) -> str:
    """
    Извлекает человекочитаемое сообщение из DRF-ошибки.

    Args:
        data:
            Данные ошибки.

    Returns:
        str: Текст ошибки.
    """

    if isinstance(data, dict):
        detail = data.get("detail")

        if detail:
            return str(detail)

        first_key = next(iter(data), None)

        if first_key:
            first_value = data[first_key]

            if isinstance(first_value, list) and first_value:
                return str(first_value[0])

            return str(first_value)

    if isinstance(data, list) and data:
        return str(data[0])

    return "Произошла ошибка при обработке запроса."