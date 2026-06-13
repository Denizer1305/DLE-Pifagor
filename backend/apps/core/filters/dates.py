from __future__ import annotations

import django_filters


class CreatedAtRangeFilterMixin(django_filters.FilterSet):
    """
    Mixin фильтрации по диапазону даты создания.

    Добавляет фильтры:
    - created_at_after;
    - created_at_before.
    """

    created_at_after = django_filters.IsoDateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        label="Создано после",
    )
    created_at_before = django_filters.IsoDateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
        label="Создано до",
    )


class UpdatedAtRangeFilterMixin(django_filters.FilterSet):
    """
    Mixin фильтрации по диапазону даты обновления.

    Добавляет фильтры:
    - updated_at_after;
    - updated_at_before.
    """

    updated_at_after = django_filters.IsoDateTimeFilter(
        field_name="updated_at",
        lookup_expr="gte",
        label="Обновлено после",
    )
    updated_at_before = django_filters.IsoDateTimeFilter(
        field_name="updated_at",
        lookup_expr="lte",
        label="Обновлено до",
    )