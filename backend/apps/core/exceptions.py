from dataclasses import dataclass
from typing import Any


@dataclass
class ErrorDetail:
    """
    Структура детализации ошибки приложения.

    Используется для передачи понятной информации об ошибке
    из сервисного слоя в API-слой.

    Attributes:
        code:
            Машинный код ошибки.
        message:
            Человекочитаемое сообщение.
        details:
            Дополнительные данные ошибки.
    """

    code: str
    message: str
    details: dict[str, Any] | None = None


class ApplicationError(Exception):
    """
    Базовое исключение приложения.

    Используется в сервисном слое, когда нужно явно остановить
    бизнес-операцию и вернуть понятную ошибку на уровень API.

    Args:
        message:
            Человекочитаемое сообщение ошибки.
        code:
            Машинный код ошибки.
        details:
            Дополнительные данные ошибки.
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

        Returns:
            ErrorDetail: Структурированная ошибка.
        """

        return ErrorDetail(
            code=self.code,
            message=self.message,
            details=self.details,
        )


class ValidationApplicationError(ApplicationError):
    """
    Исключение для ошибок бизнес-валидации.

    Пример:
        - неверный код приглашения;
        - недоступная роль;
        - недопустимый переход статуса.
    """

    default_code = "validation_error"
    default_message = "Данные не прошли проверку."


class PermissionApplicationError(ApplicationError):
    """
    Исключение для ошибок доступа.

    Используется, когда пользователь не имеет права выполнить действие.
    """

    default_code = "permission_denied"
    default_message = "У вас нет прав для выполнения этого действия."


class NotFoundApplicationError(ApplicationError):
    """
    Исключение для ситуации, когда объект не найден.

    Используется в selectors/services вместо прямой привязки
    к Django Http404 там, где нужна доменная ошибка.
    """

    default_code = "not_found"
    default_message = "Объект не найден."


class ConflictApplicationError(ApplicationError):
    """
    Исключение для конфликтов состояния.

    Пример:
        - объект уже подтверждён;
        - заявка уже обработана;
        - расписание пересекается с другим занятием.
    """

    default_code = "conflict"
    default_message = "Операция конфликтует с текущим состоянием объекта."


class RateLimitApplicationError(ApplicationError):
    """
    Исключение для превышения лимита запросов.

    Пример:
        - слишком много попыток ввода кода организации;
        - слишком много запросов подтверждения email.
    """

    default_code = "rate_limit_exceeded"
    default_message = "Превышено допустимое количество запросов."


class ExternalServiceApplicationError(ApplicationError):
    """
    Исключение для ошибок внешних сервисов.

    Пример:
        - ошибка email-провайдера;
        - ошибка SMS-провайдера;
        - ошибка AI-провайдера.
    """

    default_code = "external_service_error"
    default_message = "Внешний сервис временно недоступен."
