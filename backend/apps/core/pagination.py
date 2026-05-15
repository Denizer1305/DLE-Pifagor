from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from core.constants import DEFAULT_PAGE_SIZE, LARGE_PAGE_SIZE, MAX_LARGE_PAGE_SIZE, MAX_PAGE_SIZE


class DefaultPageNumberPagination(PageNumberPagination):
    """
    Стандартная пагинация для большинства списков API.

    Использует параметры:
        page:
            Номер страницы.
        page_size:
            Размер страницы.

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

        Args:
            data:
                Сериализованные данные текущей страницы.

        Returns:
            Response: Ответ с данными и мета-информацией.
        """

        return Response(
            OrderedDict(
                [
                    ("data", data),
                    (
                        "meta",
                        OrderedDict(
                            [
                                ("count", self.page.paginator.count),
                                ("page", self.page.number),
                                ("page_size", self.get_page_size(self.request)),
                                ("num_pages", self.page.paginator.num_pages),
                                ("next", self.get_next_link()),
                                ("previous", self.get_previous_link()),
                            ]
                        ),
                    ),
                ]
            )
        )


class LargePageNumberPagination(DefaultPageNumberPagination):
    """
    Увеличенная пагинация для административных списков.

    Используется там, где администратору нужно видеть больше записей
    на одной странице, но всё равно нужен верхний предел.
    """

    page_size = LARGE_PAGE_SIZE
    max_page_size = MAX_LARGE_PAGE_SIZE
