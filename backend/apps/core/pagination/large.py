from __future__ import annotations

from apps.core.constants import (
    LARGE_PAGE_SIZE,
    MAX_LARGE_PAGE_SIZE,
)
from apps.core.pagination.page_number import DefaultPageNumberPagination


class LargePageNumberPagination(DefaultPageNumberPagination):
    """
    Увеличенная пагинация для административных списков.

    Используется там, где администратору нужно видеть больше записей
    на одной странице, но всё равно нужен верхний предел.
    """

    page_size = LARGE_PAGE_SIZE
    max_page_size = MAX_LARGE_PAGE_SIZE