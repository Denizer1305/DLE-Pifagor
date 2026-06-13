from __future__ import annotations

from apps.core.exceptions.base import ApplicationError


class ValidationApplicationError(ApplicationError):
    """
    Исключение для ошибок бизнес-валидации.

    Примеры:
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

    Примеры:
    - объект уже подтверждён;
    - заявка уже обработана;
    - операция конфликтует с текущим состоянием.
    """

    default_code = "conflict"
    default_message = "Операция конфликтует с текущим состоянием объекта."


class RateLimitApplicationError(ApplicationError):
    """
    Исключение для превышения лимита запросов.
    """

    default_code = "rate_limit_exceeded"
    default_message = "Превышено допустимое количество запросов."


class ExternalServiceApplicationError(ApplicationError):
    """
    Исключение для ошибок внешних сервисов.
    """

    default_code = "external_service_error"
    default_message = "Внешний сервис временно недоступен."