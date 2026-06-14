from __future__ import annotations

import django_filters


class IsActiveFilterMixin(django_filters.FilterSet):
    """
    Mixin фильтрации по полю is_active.

    Требует, чтобы у модели было поле `is_active`.
    """

    is_active = django_filters.BooleanFilter(
        field_name="is_active",
        lookup_expr="exact",
        label="Активен",
    )


class IsArchivedFilterMixin(django_filters.FilterSet):
    """
    Mixin фильтрации по архивным объектам.

    Ожидает, что у модели есть поле `archived_at`.
    """

    is_archived = django_filters.BooleanFilter(
        method="filter_is_archived",
        label="В архиве",
    )

    def filter_is_archived(self, queryset, name, value):
        """
        Фильтрует объекты по признаку архивности.
        """

        if value is True:
            return queryset.filter(archived_at__isnull=False)

        if value is False:
            return queryset.filter(archived_at__isnull=True)

        return queryset


class IsDeletedFilterMixin(django_filters.FilterSet):
    """
    Mixin фильтрации по мягко удалённым объектам.

    Ожидает, что у модели есть поле `deleted_at`.
    """

    is_deleted = django_filters.BooleanFilter(
        method="filter_is_deleted",
        label="Удалён",
    )

    def filter_is_deleted(self, queryset, name, value):
        """
        Фильтрует объекты по признаку мягкого удаления.
        """

        if value is True:
            return queryset.filter(deleted_at__isnull=False)

        if value is False:
            return queryset.filter(deleted_at__isnull=True)

        return queryset
