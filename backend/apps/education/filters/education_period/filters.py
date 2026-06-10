from __future__ import annotations

import django_filters
from apps.education.models import EducationPeriod
from django.db.models import Q, QuerySet


class EducationPeriodFilter(django_filters.FilterSet):
    """
    Фильтры учебных периодов.
    """

    search = django_filters.CharFilter(method="filter_search")

    academic_year_id = django_filters.NumberFilter(
        field_name="academic_year_id",
    )
    period_type = django_filters.ChoiceFilter(
        choices=EducationPeriod.PeriodTypeChoices.choices,
    )
    sequence = django_filters.NumberFilter()

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
            ("academic_year__start_date", "academic_year_start_date"),
            ("sequence", "sequence"),
            ("start_date", "start_date"),
            ("end_date", "end_date"),
            ("name", "name"),
            ("created_at", "created_at"),
            ("updated_at", "updated_at"),
        ),
    )

    class Meta:
        model = EducationPeriod
        fields = (
            "search",
            "academic_year_id",
            "period_type",
            "sequence",
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
        Ищет период по названию, коду и учебному году.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(name__icontains=value)
            | Q(code__icontains=value)
            | Q(description__icontains=value)
            | Q(academic_year__name__icontains=value)
        )
