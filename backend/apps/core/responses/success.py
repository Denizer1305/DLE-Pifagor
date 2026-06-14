from __future__ import annotations

from typing import Any

from apps.core.constants import API_META_KEY, API_SUCCESS_KEY
from rest_framework import status
from rest_framework.response import Response


def build_success_payload(
    data: Any = None,
    *,
    meta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Формирует payload успешного API-ответа.
    """

    payload: dict[str, Any] = {
        API_SUCCESS_KEY: data,
    }

    if meta is not None:
        payload[API_META_KEY] = meta

    return payload


def success_response(
    data: Any = None,
    *,
    meta: dict[str, Any] | None = None,
    status_code: int = status.HTTP_200_OK,
) -> Response:
    """
    Формирует единый успешный API-ответ.
    """

    return Response(
        build_success_payload(
            data=data,
            meta=meta,
        ),
        status=status_code,
    )


def created_response(
    data: Any = None,
    *,
    meta: dict[str, Any] | None = None,
) -> Response:
    """
    Формирует ответ для успешно созданного объекта.
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
    """

    return Response(status=status_code)
