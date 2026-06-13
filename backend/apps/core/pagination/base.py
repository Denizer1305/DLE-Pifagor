from __future__ import annotations

from collections import OrderedDict
from typing import Any

from apps.core.constants import (
    API_META_KEY,
    API_SUCCESS_KEY,
)
from rest_framework.response import Response


def build_pagination_meta(paginator) -> OrderedDict[str, Any]:
    """
    Формирует meta-блок для постраничной пагинации.
    """

    return OrderedDict(
        [
            ("count", paginator.page.paginator.count),
            ("page", paginator.page.number),
            ("page_size", paginator.get_page_size(paginator.request)),
            ("num_pages", paginator.page.paginator.num_pages),
            ("next", paginator.get_next_link()),
            ("previous", paginator.get_previous_link()),
        ]
    )


def paginated_response(paginator, data) -> Response:
    """
    Формирует единый ответ постраничной пагинации.
    """

    return Response(
        OrderedDict(
            [
                (API_SUCCESS_KEY, data),
                (API_META_KEY, build_pagination_meta(paginator)),
            ]
        )
    )