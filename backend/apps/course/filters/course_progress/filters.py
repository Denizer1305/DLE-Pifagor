from __future__ import annotations

import django_filters
from apps.course.models import CourseProgress


class CourseProgressFilter(django_filters.FilterSet):
    """
    Фильтры общего прогресса курса.
    """

    enrollment_id = django_filters.NumberFilter(field_name="enrollment_id")
    course_id = django_filters.NumberFilter(field_name="enrollment__course_id")
    learner_id = django_filters.NumberFilter(field_name="enrollment__learner_id")
    last_lesson_id = django_filters.NumberFilter(field_name="last_lesson_id")

    progress_min = django_filters.NumberFilter(
        field_name="progress_percent",
        lookup_expr="gte",
    )
    progress_max = django_filters.NumberFilter(
        field_name="progress_percent",
        lookup_expr="lte",
    )
    completed = django_filters.BooleanFilter(method="filter_completed")

    last_activity_after = django_filters.DateTimeFilter(
        field_name="last_activity_at",
        lookup_expr="gte",
    )
    last_activity_before = django_filters.DateTimeFilter(
        field_name="last_activity_at",
        lookup_expr="lte",
    )

    class Meta:
        model = CourseProgress
        fields = (
            "enrollment_id",
            "course_id",
            "learner_id",
            "last_lesson_id",
            "progress_min",
            "progress_max",
            "completed",
            "last_activity_after",
            "last_activity_before",
        )

    def filter_completed(self, queryset, name: str, value: bool):
        """
        Фильтрует завершённые и незавершённые курсы.
        """

        if value:
            return queryset.filter(progress_percent=100)

        return queryset.filter(progress_percent__lt=100)
