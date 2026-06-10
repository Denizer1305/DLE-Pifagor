from __future__ import annotations

import django_filters
from apps.course.models import CourseAccessRule
from django.db.models import Q


class CourseAccessRuleFilter(django_filters.FilterSet):
    """
    Фильтры правил доступа к курсам.
    """

    search = django_filters.CharFilter(method="filter_search")

    course_id = django_filters.NumberFilter(field_name="course_id")
    access_type = django_filters.ChoiceFilter(
        field_name="access_type",
        choices=CourseAccessRule.AccessTypeChoices.choices,
    )
    learner_id = django_filters.NumberFilter(field_name="learner_id")
    organization_id = django_filters.NumberFilter(field_name="organization_id")

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
        model = CourseAccessRule
        fields = (
            "search",
            "course_id",
            "access_type",
            "learner_id",
            "organization_id",
            "auto_enroll",
            "is_active",
            "starts_after",
            "starts_before",
            "ends_after",
            "ends_before",
        )

    def filter_search(self, queryset, name: str, value: str):
        """
        Ищет правило доступа по курсу, пользователю, организации и коду.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(course__title__icontains=value)
            | Q(course__code__icontains=value)
            | Q(access_code__icontains=value)
            | Q(learner__email__icontains=value)
            | Q(learner__first_name__icontains=value)
            | Q(learner__last_name__icontains=value)
            | Q(organization__name__icontains=value)
            | Q(organization__short_name__icontains=value)
            | Q(organization__code__icontains=value)
            | Q(notes__icontains=value)
        )
