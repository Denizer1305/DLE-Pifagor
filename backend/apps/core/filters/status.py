from __future__ import annotations

import django_filters


class StatusFilterMixin(django_filters.FilterSet):
    """
    Mixin фильтрации по полю status.

    Требует, чтобы у модели было поле `status`.
    """

    status = django_filters.CharFilter(
        field_name="status",
        lookup_expr="exact",
        label="Статус",
    )