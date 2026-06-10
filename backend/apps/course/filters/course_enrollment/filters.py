from __future__ import annotations

import django_filters
from apps.course.models import CourseEnrollment
from django.db.models import Q


class CourseEnrollmentFilter(django_filters.FilterSet):
    """
    Фильтры записей на курс.
    """

    search = django_filters.CharFilter(method="filter_search")

    course_id = django_filters.NumberFilter(field_name="course_id")
    learner_id = django_filters.NumberFilter(field_name="learner_id")
    group_access_id = django_filters.NumberFilter(field_name="group_access_id")
    access_rule_id = django_filters.NumberFilter(field_name="access_rule_id")

    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=CourseEnrollment.StatusChoices.choices,
    )

    progress_min = django_filters.NumberFilter(
        field_name="progress_percent",
        lookup_expr="gte",
    )
    progress_max = django_filters.NumberFilter(
        field_name="progress_percent",
        lookup_expr="lte",
    )

    enrolled_after = django_filters.DateTimeFilter(
        field_name="enrolled_at",
        lookup_expr="gte",
    )
    enrolled_before = django_filters.DateTimeFilter(
        field_name="enrolled_at",
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

    class Meta:
        model = CourseEnrollment
        fields = (
            "search",
            "course_id",
            "learner_id",
            "group_access_id",
            "access_rule_id",
            "status",
            "progress_min",
            "progress_max",
            "enrolled_after",
            "enrolled_before",
            "started_after",
            "started_before",
            "completed_after",
            "completed_before",
        )

    def filter_search(self, queryset, name: str, value: str):
        """
        Ищет запись на курс по курсу и обучающемуся.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(course__title__icontains=value)
            | Q(course__code__icontains=value)
            | Q(learner__email__icontains=value)
            | Q(learner__first_name__icontains=value)
            | Q(learner__last_name__icontains=value)
        )
