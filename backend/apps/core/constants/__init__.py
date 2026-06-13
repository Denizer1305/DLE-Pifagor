"""
Общие константы проекта.

В этом пакете должны храниться только универсальные константы,
которые не относятся к конкретному бизнес-модулю.

Например:
    - настройки пагинации;
    - стандартные сроки;
    - технические ограничения;
    - общие ключи ответа API.

Доменные константы, такие как роли пользователей или статусы заявок,
должны находиться внутри соответствующих приложений.
"""

from __future__ import annotations

from .api import (
    API_ERROR_KEY,
    API_META_KEY,
    API_SUCCESS_KEY,
)
from .dates import (
    DEFAULT_DATE_FORMAT,
    DEFAULT_DATETIME_FORMAT,
)
from .lifecycle import DEFAULT_DELETION_GRACE_DAYS
from .pagination import (
    DEFAULT_PAGE_SIZE,
    LARGE_PAGE_SIZE,
    MAX_LARGE_PAGE_SIZE,
    MAX_PAGE_SIZE,
)

__all__ = [
    "API_ERROR_KEY",
    "API_META_KEY",
    "API_SUCCESS_KEY",
    "DEFAULT_DATE_FORMAT",
    "DEFAULT_DATETIME_FORMAT",
    "DEFAULT_DELETION_GRACE_DAYS",
    "DEFAULT_PAGE_SIZE",
    "LARGE_PAGE_SIZE",
    "MAX_LARGE_PAGE_SIZE",
    "MAX_PAGE_SIZE",
]