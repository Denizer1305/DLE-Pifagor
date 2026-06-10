from __future__ import annotations

import django_filters
from apps.course.models import CourseGroupAccess
from django.db.models import Q


class CourseGroupAccessFilter(django_filters.FilterSet):
    """
    Фильтры доступа групп к курсам.
    """

    search = django_filters.CharFilter(method="filter_search")

    course_id = django_filters.NumberFilter(field_name="course_id")
    group_id = django_filters.NumberFilter(field_name="group_id")
    group_subject_id = django_filters.NumberFilter(field_name="group_subject_id")
    teacher_group_subject_id = django_filters.NumberFilter(
        field_name="teacher_group_subject_id",
    )

    visibility = django_filters.ChoiceFilter(
        field_name="visibility",
        choices=CourseGroupAccess.VisibilityChoices.choices,
    )
    auto_enroll = django_filters.BooleanFilter(field_name="auto_enroll")
    is_active = django_filters.BooleanFilter(field_name="is_active")

    starts_after = django_filters.DateTimeFilter(
        field_name="starts_at",
        lookup_expr="gte",
    )
    starts_before = django_filters.DateTimeFilter(
        field_name="starts_at",
        lookup_expr="lte",
    )
    ends_after = django_filters.DateTimeFilter(
        field_name="ends_at",
        lookup_expr="gte",
    )
    ends_before = django_filters.DateTimeFilter(
        field_name="ends_at",
        lookup_expr="lte",
    )

    class Meta:
        model = CourseGroupAccess
        fields = (
            "search",
            "course_id",
            "group_id",
            "group_subject_id",
            "teacher_group_subject_id",
            "visibility",
            "auto_enroll",
            "is_active",
            "starts_after",
            "starts_before",
            "ends_after",
            "ends_before",
        )

    def filter_search(self, queryset, name: str, value: str):
        """
        Ищет доступ группы по курсу, группе и организации.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(course__title__icontains=value)
            | Q(course__code__icontains=value)
            | Q(group__name__icontains=value)
            | Q(group__code__icontains=value)
            | Q(course__organization__name__icontains=value)
            | Q(course__organization__short_name__icontains=value)
            | Q(course__subject__name__icontains=value)
            | Q(course__subject__code__icontains=value)
            | Q(notes__icontains=value)
        )
