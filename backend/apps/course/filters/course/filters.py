from __future__ import annotations

import django_filters
from apps.course.models import Course
from django.db.models import Q


class CourseFilter(django_filters.FilterSet):
    """
    Фильтры курсов.
    """

    search = django_filters.CharFilter(method="filter_search")

    course_type = django_filters.ChoiceFilter(
        field_name="course_type",
        choices=Course.CourseTypeChoices.choices,
    )
    origin = django_filters.ChoiceFilter(
        field_name="origin",
        choices=Course.OriginChoices.choices,
    )
    status = django_filters.ChoiceFilter(
        field_name="status",
        choices=Course.StatusChoices.choices,
    )
    visibility = django_filters.ChoiceFilter(
        field_name="visibility",
        choices=Course.VisibilityChoices.choices,
    )

    organization_id = django_filters.NumberFilter(field_name="organization_id")
    subject_id = django_filters.NumberFilter(field_name="subject_id")
    academic_year_id = django_filters.NumberFilter(field_name="academic_year_id")
    period_id = django_filters.NumberFilter(field_name="period_id")
    owner_teacher_id = django_filters.NumberFilter(field_name="owner_teacher_id")

    is_template = django_filters.BooleanFilter(field_name="is_template")
    is_active = django_filters.BooleanFilter(field_name="is_active")
    allow_self_enrollment = django_filters.BooleanFilter(
        field_name="allow_self_enrollment",
    )

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

    created_after = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
    )
    created_before = django_filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="lte",
    )
    updated_after = django_filters.DateTimeFilter(
        field_name="updated_at",
        lookup_expr="gte",
    )
    updated_before = django_filters.DateTimeFilter(
        field_name="updated_at",
        lookup_expr="lte",
    )

    class Meta:
        model = Course
        fields = (
            "search",
            "course_type",
            "origin",
            "status",
            "visibility",
            "organization_id",
            "subject_id",
            "academic_year_id",
            "period_id",
            "owner_teacher_id",
            "is_template",
            "is_active",
            "allow_self_enrollment",
            "starts_after",
            "starts_before",
            "ends_after",
            "ends_before",
            "created_after",
            "created_before",
            "updated_after",
            "updated_before",
        )

    def filter_search(self, queryset, name: str, value: str):
        """
        Ищет курс по основным текстовым полям.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(title__icontains=value)
            | Q(subtitle__icontains=value)
            | Q(description__icontains=value)
            | Q(code__icontains=value)
            | Q(slug__icontains=value)
            | Q(level__icontains=value)
            | Q(language__icontains=value)
            | Q(organization__name__icontains=value)
            | Q(organization__short_name__icontains=value)
            | Q(organization__code__icontains=value)
            | Q(subject__name__icontains=value)
            | Q(subject__short_name__icontains=value)
            | Q(subject__code__icontains=value)
            | Q(owner_teacher__email__icontains=value)
            | Q(owner_teacher__first_name__icontains=value)
            | Q(owner_teacher__last_name__icontains=value)
        )
