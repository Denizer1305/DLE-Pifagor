from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class ErrorDetail:
    """
    Структура детализации ошибки приложения.

    Используется для передачи понятной информации об ошибке
    из сервисного слоя в API-слой.
    """

    code: str
    message: str
    details: dict[str, Any] | None = None


class ApplicationError(Exception):
    """
    Базовое исключение приложения.

    Используется в сервисном слое, когда нужно явно остановить
    бизнес-операцию и вернуть понятную ошибку на уровень API.
    """

    default_code = "application_error"
    default_message = "Произошла ошибка приложения."

    def __init__(
        self,
        message: str | None = None,
        *,
        code: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        self.message = message or self.default_message
        self.code = code or self.default_code
        self.details = details or {}

        super().__init__(self.message)

    def as_detail(self) -> ErrorDetail:
        """
        Возвращает ошибку в виде структуры ErrorDetail.
        """

        return ErrorDetail(
            code=self.code,
            message=self.message,
            details=self.details,
        )