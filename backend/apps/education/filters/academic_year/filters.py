from __future__ import annotations

import django_filters
from apps.education.models import AcademicYear
from django.db.models import Q, QuerySet


class AcademicYearFilter(django_filters.FilterSet):
    """
    Фильтры учебных годов.
    """

    search = django_filters.CharFilter(method="filter_search")
    start_date_from = django_filters.DateFilter(
        field_name="start_date",
        lookup_expr="gte",
    )
    start_date_to = django_filters.DateFilter(
        field_name="start_date",
        lookup_expr="lte",
    )
    end_date_from = django_filters.DateFilter(
        field_name="end_date",
        lookup_expr="gte",
    )
    end_date_to = django_filters.DateFilter(
        field_name="end_date",
        lookup_expr="lte",
    )
    is_current = django_filters.BooleanFilter()
    is_active = django_filters.BooleanFilter()

    ordering = django_filters.OrderingFilter(
        fields=(
            ("start_date", "start_date"),
            ("end_date", "end_date"),
            ("name", "name"),
            ("created_at", "created_at"),
            ("updated_at", "updated_at"),
        ),
    )

    class Meta:
        model = AcademicYear
        fields = (
            "search",
            "start_date_from",
            "start_date_to",
            "end_date_from",
            "end_date_to",
            "is_current",
            "is_active",
            "ordering",
        )

    def filter_search(
        self,
        queryset: QuerySet,
        name: str,
        value: str,
    ) -> QuerySet:
        """
        Ищет учебный год по названию и описанию.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(name__icontains=value) | Q(description__icontains=value)
        )
