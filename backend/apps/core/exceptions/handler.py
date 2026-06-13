from __future__ import annotations

from apps.core.exceptions.base import ApplicationError
from apps.core.responses import error_response
from rest_framework import status
from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    """
    Обрабатывает исключения DRF и приложения.

    Возвращает ошибки API в едином формате:

    {
        "error": {
            "code": "...",
            "message": "...",
            "details": {}
        }
    }
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
    error_message = extract_error_message(response.data)

    response.data = {
        "error": {
            "code": str(error_code),
            "message": error_message,
            "details": response.data,
        }
    }

    return response


def extract_error_message(data) -> str:
    """
    Извлекает человекочитаемое сообщение из DRF-ошибки.
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
