from __future__ import annotations

import django_filters
from apps.course.models import CoursePlan
from django.db.models import Q


class CoursePlanFilter(django_filters.FilterSet):
    """
    Фильтры КТП курса.
    """

    search = django_filters.CharFilter(method="filter_search")

    course_id = django_filters.NumberFilter(field_name="course_id")
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=CoursePlan.StatusChoices.choices,
    )
    semester_number = django_filters.NumberFilter(field_name="semester_number")
    is_active = django_filters.BooleanFilter(field_name="is_active")

    total_hours_min = django_filters.NumberFilter(
        field_name="total_hours",
        lookup_expr="gte",
    )
    total_hours_max = django_filters.NumberFilter(
        field_name="total_hours",
        lookup_expr="lte",
    )

    class Meta:
        model = CoursePlan
        fields = (
            "search",
            "course_id",
            "status",
            "semester_number",
            "is_active",
            "total_hours_min",
            "total_hours_max",
        )

    def filter_search(self, queryset, name: str, value: str):
        """
        Ищет КТП по курсу, дисциплине, специальности и снимкам данных.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(course__title__icontains=value)
            | Q(course__code__icontains=value)
            | Q(discipline_name__icontains=value)
            | Q(discipline_code__icontains=value)
            | Q(specialty_code__icontains=value)
            | Q(specialty_name__icontains=value)
            | Q(teacher_name_snapshot__icontains=value)
            | Q(organization_name_snapshot__icontains=value)
            | Q(academic_year_label__icontains=value)
            | Q(commission_name__icontains=value)
            | Q(protocol_number__icontains=value)
            | Q(approved_order_number__icontains=value)
            | Q(notes__icontains=value)
        )
