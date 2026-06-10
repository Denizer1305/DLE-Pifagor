from __future__ import annotations

import django_filters
from apps.materials.models import MaterialCategory
from django.db.models import Q


class MaterialCategoryFilter(django_filters.FilterSet):
    """
    Фильтры категорий учебных материалов.
    """

    search = django_filters.CharFilter(method="filter_search")

    organization_id = django_filters.NumberFilter(
        field_name="organization_id",
    )
    parent_id = django_filters.NumberFilter(
        field_name="parent_id",
    )
    is_active = django_filters.BooleanFilter(
        field_name="is_active",
    )
    global_only = django_filters.BooleanFilter(
        method="filter_global_only",
    )
    root_only = django_filters.BooleanFilter(
        method="filter_root_only",
    )

    class Meta:
        model = MaterialCategory
        fields = (
            "search",
            "organization_id",
            "parent_id",
            "is_active",
            "global_only",
            "root_only",
        )

    def filter_search(
        self,
        queryset,
        name: str,
        value: str,
    ):
        """
        Ищет категорию по названию, slug, описанию или организации.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(name__icontains=value)
            | Q(slug__icontains=value)
            | Q(description__icontains=value)
            | Q(organization__name__icontains=value)
            | Q(organization__short_name__icontains=value)
            | Q(organization__code__icontains=value)
        )

    def filter_global_only(
        self,
        queryset,
        name: str,
        value: bool,
    ):
        """
        Оставляет только глобальные категории.
        """

        if value:
            return queryset.filter(organization__isnull=True)

        return queryset

    def filter_root_only(
        self,
        queryset,
        name: str,
        value: bool,
    ):
        """
        Оставляет только корневые категории.
        """

        if value:
            return queryset.filter(parent__isnull=True)

        return queryset
