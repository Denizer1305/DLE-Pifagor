from __future__ import annotations

import django_filters
from apps.course.models import LessonProgress


class LessonProgressFilter(django_filters.FilterSet):
    """
    Фильтры прогресса уроков.
    """

    enrollment_id = django_filters.NumberFilter(field_name="enrollment_id")
    course_progress_id = django_filters.NumberFilter(
        field_name="course_progress_id",
    )
    lesson_id = django_filters.NumberFilter(field_name="lesson_id")
    course_id = django_filters.NumberFilter(field_name="enrollment__course_id")
    learner_id = django_filters.NumberFilter(field_name="enrollment__learner_id")

    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=LessonProgress.StatusChoices.choices,
    )

    progress_min = django_filters.NumberFilter(
        field_name="progress_percent",
        lookup_expr="gte",
    )
    progress_max = django_filters.NumberFilter(
        field_name="progress_percent",
        lookup_expr="lte",
    )

    started_after = django_filters.DateTimeFilter(
        field_name="started_at",
        lookup_expr="gte",
    )
    started_before = django_filters.DateTimeFilter(
        field_name="started_at",
        lookup_expr="lte",
    )
    completed_after = django_filters.DateTimeFilter(
        field_name="completed_at",
        lookup_expr="gte",
    )
    completed_before = django_filters.DateTimeFilter(
        field_name="completed_at",
        lookup_expr="lte",
    )
    last_activity_after = django_filters.DateTimeFilter(
        field_name="last_activity_at",
        lookup_expr="gte",
    )
    last_activity_before = django_filters.DateTimeFilter(
        field_name="last_activity_at",
        lookup_expr="lte",
    )

    class Meta:
        model = LessonProgress
        fields = (
            "enrollment_id",
            "course_progress_id",
            "lesson_id",
            "course_id",
            "learner_id",
            "status",
            "progress_min",
            "progress_max",
            "started_after",
            "started_before",
            "completed_after",
            "completed_before",
            "last_activity_after",
            "last_activity_before",
        )
