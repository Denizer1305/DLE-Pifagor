from __future__ import annotations

import django_filters
from apps.course.models import CourseSection
from django.db.models import Q


class CourseSectionFilter(django_filters.FilterSet):
    """
    Фильтры разделов курса.
    """

    search = django_filters.CharFilter(method="filter_search")

    course_id = django_filters.NumberFilter(field_name="course_id")
    is_required = django_filters.BooleanFilter(field_name="is_required")
    is_published = django_filters.BooleanFilter(field_name="is_published")
    is_active = django_filters.BooleanFilter(field_name="is_active")

    planned_hours_min = django_filters.NumberFilter(
        field_name="planned_hours",
        lookup_expr="gte",
    )
    planned_hours_max = django_filters.NumberFilter(
        field_name="planned_hours",
        lookup_expr="lte",
    )

    class Meta:
        model = CourseSection
        fields = (
            "search",
            "course_id",
            "is_required",
            "is_published",
            "is_active",
            "planned_hours_min",
            "planned_hours_max",
        )

    def filter_search(self, queryset, name: str, value: str):
        """
        Ищет раздел по названию, описанию и курсу.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(title__icontains=value)
            | Q(description__icontains=value)
            | Q(course__title__icontains=value)
            | Q(course__code__icontains=value)
        )
