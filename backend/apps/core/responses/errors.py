from __future__ import annotations

from typing import Any

from apps.core.constants import API_ERROR_KEY
from apps.core.exceptions import ApplicationError
from rest_framework import status
from rest_framework.response import Response


def build_error_payload(
    *,
    code: str,
    message: str,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Формирует payload ошибки API.
    """

    return {
        API_ERROR_KEY: {
            "code": code,
            "message": message,
            "details": details or {},
        }
    }


def error_response(
    *,
    code: str,
    message: str,
    details: dict[str, Any] | None = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> Response:
    """
    Формирует единый API-ответ с ошибкой.
    """

    return Response(
        build_error_payload(
            code=code,
            message=message,
            details=details,
        ),
        status=status_code,
    )


def application_error_response(
    error: ApplicationError,
    *,
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> Response:
    """
    Преобразует ApplicationError в API-ответ.
    """

    return error_response(
        code=error.code,
        message=error.message,
        details=error.details,
        status_code=status_code,
    )