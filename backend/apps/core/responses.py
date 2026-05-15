from typing import Any

from core.constants import API_ERROR_KEY, API_META_KEY, API_SUCCESS_KEY
from core.exceptions import ApplicationError
from rest_framework import status
from rest_framework.response import Response


def success_response(
    data: Any = None,
    *,
    meta: dict[str, Any] | None = None,
    status_code: int = status.HTTP_200_OK,
) -> Response:
    """
    Формирует единый успешный API-ответ.

    Args:
        data:
            Основные данные ответа.
        meta:
            Дополнительная мета-информация.
        status_code:
            HTTP-статус ответа.

    Returns:
        Response: DRF Response в едином формате.
    """

    payload: dict[str, Any] = {
        API_SUCCESS_KEY: data,
    }

    if meta is not None:
        payload[API_META_KEY] = meta

    return Response(payload, status=status_code)


def created_response(
    data: Any = None,
    *,
    meta: dict[str, Any] | None = None,
) -> Response:
    """
    Формирует ответ для успешно созданного объекта.

    Args:
        data:
            Данные созданного объекта.
        meta:
            Дополнительная мета-информация.

    Returns:
        Response: Ответ с HTTP 201.
    """

    return success_response(
        data=data,
        meta=meta,
        status_code=status.HTTP_201_CREATED,
    )


def empty_response(
    *,
    status_code: int = status.HTTP_204_NO_CONTENT,
) -> Response:
    """
    Формирует пустой ответ.

    Обычно используется после удаления, выхода из системы
    или успешного действия без тела ответа.

    Args:
        status_code:
            HTTP-статус ответа.

    Returns:
        Response: Пустой DRF Response.
    """

    return Response(status=status_code)


def error_response(
    *,
    code: str,
    message: str,
    details: dict[str, Any] | None = None,
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> Response:
    """
    Формирует единый API-ответ с ошибкой.

    Args:
        code:
            Машинный код ошибки.
        message:
            Человекочитаемое сообщение.
        details:
            Дополнительные данные ошибки.
        status_code:
            HTTP-статус ответа.

    Returns:
        Response: DRF Response с ошибкой.
    """

    return Response(
        {
            API_ERROR_KEY: {
                "code": code,
                "message": message,
                "details": details or {},
            }
        },
        status=status_code,
    )


def application_error_response(
    error: ApplicationError,
    *,
    status_code: int = status.HTTP_400_BAD_REQUEST,
) -> Response:
    """
    Преобразует ApplicationError в API-ответ.

    Args:
        error:
            Исключение приложения.
        status_code:
            HTTP-статус ответа.

    Returns:
        Response: DRF Response с ошибкой.
    """

    return error_response(
        code=error.code,
        message=error.message,
        details=error.details,
        status_code=status_code,
    )
