from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from apps.core.utils import generate_uuid_string


@dataclass(slots=True)
class BackofficeUserBulkItemResult:
    """
    Результат обработки одного пользователя в bulk-операции.
    """

    user_id: int
    success: bool
    action: str
    message: str = ""
    error_code: str = ""
    errors: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        """
        Возвращает результат в виде dict для serializer/API.
        """

        return asdict(self)


@dataclass(slots=True)
class BackofficeUserBulkResult:
    """
    Итоговый результат bulk-операции.
    """

    action: str
    items: list[BackofficeUserBulkItemResult]
    bulk_action_id: str = field(default_factory=generate_uuid_string)

    @property
    def total_count(self) -> int:
        """
        Возвращает общее количество обработанных пользователей.
        """

        return len(self.items)

    @property
    def success_count(self) -> int:
        """
        Возвращает количество успешно обработанных пользователей.
        """

        return sum(1 for item in self.items if item.success)

    @property
    def failed_count(self) -> int:
        """
        Возвращает количество ошибок.
        """

        return sum(1 for item in self.items if not item.success)

    def as_dict(self) -> dict[str, Any]:
        """
        Возвращает итог bulk-операции в виде dict.
        """

        return {
            "action": self.action,
            "bulk_action_id": self.bulk_action_id,
            "total_count": self.total_count,
            "success_count": self.success_count,
            "failed_count": self.failed_count,
            "items": [item.as_dict() for item in self.items],
        }


def build_success_bulk_item_result(
    *,
    user_id: int,
    action: str,
    message: str = "",
) -> BackofficeUserBulkItemResult:
    """
    Формирует успешный результат обработки одного пользователя.
    """

    return BackofficeUserBulkItemResult(
        user_id=user_id,
        success=True,
        action=action,
        message=message,
    )


def build_failed_bulk_item_result(
    *,
    user_id: int,
    action: str,
    message: str,
    error_code: str = "bulk_item_error",
    errors: dict[str, Any] | None = None,
) -> BackofficeUserBulkItemResult:
    """
    Формирует результат ошибки обработки одного пользователя.
    """

    return BackofficeUserBulkItemResult(
        user_id=user_id,
        success=False,
        action=action,
        message=message,
        error_code=error_code,
        errors=errors or {},
    )


# Совместимые alias'ы.
AdminUserBulkItemResult = BackofficeUserBulkItemResult
AdminUserBulkResult = BackofficeUserBulkResult
