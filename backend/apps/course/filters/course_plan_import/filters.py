from __future__ import annotations

import django_filters
from apps.course.models import CoursePlanImport
from django.db.models import Q


class CoursePlanImportFilter(django_filters.FilterSet):
    """
    Фильтры импортов КТП.
    """

    search = django_filters.CharFilter(method="filter_search")

    course_plan_id = django_filters.NumberFilter(field_name="course_plan_id")
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=CoursePlanImport.StatusChoices.choices,
    )
    imported_by_id = django_filters.NumberFilter(field_name="imported_by_id")

    imported_after = django_filters.DateTimeFilter(
        field_name="imported_at",
        lookup_expr="gte",
    )
    imported_before = django_filters.DateTimeFilter(
        field_name="imported_at",
        lookup_expr="lte",
    )
    applied_after = django_filters.DateTimeFilter(
        field_name="applied_at",
        lookup_expr="gte",
    )
    applied_before = django_filters.DateTimeFilter(
        field_name="applied_at",
        lookup_expr="lte",
    )

    class Meta:
        model = CoursePlanImport
        fields = (
            "search",
            "course_plan_id",
            "status",
            "imported_by_id",
            "imported_after",
            "imported_before",
            "applied_after",
            "applied_before",
        )

    def filter_search(self, queryset, name: str, value: str):
        """
        Ищет импорт КТП по файлу, курсу, версии парсера и пользователю.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(course_plan__course__title__icontains=value)
            | Q(course_plan__course__code__icontains=value)
            | Q(original_filename__icontains=value)
            | Q(file_hash__icontains=value)
            | Q(parser_version__icontains=value)
            | Q(imported_by__email__icontains=value)
            | Q(imported_by__first_name__icontains=value)
            | Q(imported_by__last_name__icontains=value)
        )
