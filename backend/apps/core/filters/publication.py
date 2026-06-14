from __future__ import annotations

import django_filters


class IsPublishedFilterMixin(django_filters.FilterSet):
    """
    Mixin фильтрации по опубликованным объектам.

    Ожидает, что у модели есть поле `published_at`.
    """

    is_published = django_filters.BooleanFilter(
        method="filter_is_published",
        label="Опубликован",
    )

    def filter_is_published(self, queryset, name, value):
        """
        Фильтрует объекты по признаку публикации.
        """

        if value is True:
            return queryset.filter(published_at__isnull=False)

        if value is False:
            return queryset.filter(published_at__isnull=True)

        return queryset
