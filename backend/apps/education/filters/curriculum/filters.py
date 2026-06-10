from __future__ import annotations

import django_filters
from apps.education.models import Curriculum
from django.db.models import Q, QuerySet


class CurriculumFilter(django_filters.FilterSet):
    """
    Фильтры учебных планов.
    """

    search = django_filters.CharFilter(method="filter_search")

    organization_id = django_filters.NumberFilter(
        field_name="organization_id",
    )
    department_id = django_filters.NumberFilter(
        field_name="department_id",
    )
    academic_year_id = django_filters.NumberFilter(
        field_name="academic_year_id",
    )

    status = django_filters.ChoiceFilter(
        choices=Curriculum.StatusChoices.choices,
    )
    is_active = django_filters.BooleanFilter()

    total_hours_from = django_filters.NumberFilter(
        field_name="total_hours",
        lookup_expr="gte",
    )
    total_hours_to = django_filters.NumberFilter(
        field_name="total_hours",
        lookup_expr="lte",
    )

    ordering = django_filters.OrderingFilter(
        fields=(
            ("organization__name", "organization"),
            ("department__name", "department"),
            ("academic_year__start_date", "academic_year_start_date"),
            ("name", "name"),
            ("code", "code"),
            ("status", "status"),
            ("total_hours", "total_hours"),
            ("created_at", "created_at"),
            ("updated_at", "updated_at"),
        ),
    )

    class Meta:
        model = Curriculum
        fields = (
            "search",
            "organization_id",
            "department_id",
            "academic_year_id",
            "status",
            "is_active",
            "total_hours_from",
            "total_hours_to",
            "ordering",
        )

    def filter_search(
        self,
        queryset: QuerySet,
        name: str,
        value: str,
    ) -> QuerySet:
        """
        Ищет учебный план по названию, коду, организации и отделению.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(name__icontains=value)
            | Q(code__icontains=value)
            | Q(description__icontains=value)
            | Q(organization__name__icontains=value)
            | Q(organization__short_name__icontains=value)
            | Q(organization__code__icontains=value)
            | Q(department__name__icontains=value)
            | Q(department__short_name__icontains=value)
            | Q(department__code__icontains=value)
            | Q(academic_year__name__icontains=value)
        )
