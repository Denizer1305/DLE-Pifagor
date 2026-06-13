from __future__ import annotations

from apps.core.constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE
from apps.core.pagination.base import paginated_response
from rest_framework.pagination import PageNumberPagination


class DefaultPageNumberPagination(PageNumberPagination):
    """
    Стандартная пагинация для большинства списков API.

    Использует параметры:
    - page;
    - page_size.

    Ограничивает максимальный размер страницы, чтобы пользователь
    не мог случайно или намеренно запросить слишком большой объём данных.
    """

    page_size = DEFAULT_PAGE_SIZE
    page_query_param = "page"
    page_size_query_param = "page_size"
    max_page_size = MAX_PAGE_SIZE

    def get_paginated_response(self, data):
        """
        Возвращает ответ пагинации в едином формате проекта.
        """

        return paginated_response(
            paginator=self,
            data=data,
        )
