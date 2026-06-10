from __future__ import annotations

import django_filters
from apps.education.models import TeacherGroupSubject
from django.db.models import Q, QuerySet


class TeacherGroupSubjectFilter(django_filters.FilterSet):
    """
    Фильтры назначений преподавателей на предметы групп.
    """

    search = django_filters.CharFilter(method="filter_search")

    teacher_id = django_filters.NumberFilter(
        field_name="teacher_id",
    )
    group_subject_id = django_filters.NumberFilter(
        field_name="group_subject_id",
    )
    organization_id = django_filters.NumberFilter(
        field_name="group_subject__group__organization_id",
    )
    department_id = django_filters.NumberFilter(
        field_name="group_subject__group__department_id",
    )
    group_id = django_filters.NumberFilter(
        field_name="group_subject__group_id",
    )
    subject_id = django_filters.NumberFilter(
        field_name="group_subject__subject_id",
    )
    academic_year_id = django_filters.NumberFilter(
        field_name="group_subject__academic_year_id",
    )
    period_id = django_filters.NumberFilter(
        field_name="group_subject__period_id",
    )

    role = django_filters.ChoiceFilter(
        choices=TeacherGroupSubject.RoleChoices.choices,
    )
    is_primary = django_filters.BooleanFilter()
    is_active = django_filters.BooleanFilter()

    planned_hours_from = django_filters.NumberFilter(
        field_name="planned_hours",
        lookup_expr="gte",
    )
    planned_hours_to = django_filters.NumberFilter(
        field_name="planned_hours",
        lookup_expr="lte",
    )
    starts_at_from = django_filters.DateFilter(
        field_name="starts_at",
        lookup_expr="gte",
    )
    starts_at_to = django_filters.DateFilter(
        field_name="starts_at",
        lookup_expr="lte",
    )
    ends_at_from = django_filters.DateFilter(
        field_name="ends_at",
        lookup_expr="gte",
    )
    ends_at_to = django_filters.DateFilter(
        field_name="ends_at",
        lookup_expr="lte",
    )

    ordering = django_filters.OrderingFilter(
        fields=(
            ("teacher__last_name", "teacher"),
            ("group_subject__group__name", "group"),
            ("group_subject__subject__name", "subject"),
            ("group_subject__academic_year__start_date", "academic_year_start_date"),
            ("group_subject__period__sequence", "period_sequence"),
            ("role", "role"),
            ("is_primary", "is_primary"),
            ("planned_hours", "planned_hours"),
            ("starts_at", "starts_at"),
            ("ends_at", "ends_at"),
            ("created_at", "created_at"),
            ("updated_at", "updated_at"),
        ),
    )

    class Meta:
        model = TeacherGroupSubject
        fields = (
            "search",
            "teacher_id",
            "group_subject_id",
            "organization_id",
            "department_id",
            "group_id",
            "subject_id",
            "academic_year_id",
            "period_id",
            "role",
            "is_primary",
            "is_active",
            "planned_hours_from",
            "planned_hours_to",
            "starts_at_from",
            "starts_at_to",
            "ends_at_from",
            "ends_at_to",
            "ordering",
        )

    def filter_search(
        self,
        queryset: QuerySet,
        name: str,
        value: str,
    ) -> QuerySet:
        """
        Ищет назначение преподавателя.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(teacher__email__icontains=value)
            | Q(teacher__first_name__icontains=value)
            | Q(teacher__last_name__icontains=value)
            | Q(group_subject__group__name__icontains=value)
            | Q(group_subject__group__code__icontains=value)
            | Q(group_subject__subject__name__icontains=value)
            | Q(group_subject__subject__short_name__icontains=value)
            | Q(group_subject__subject__code__icontains=value)
            | Q(group_subject__period__name__icontains=value)
            | Q(group_subject__period__code__icontains=value)
            | Q(notes__icontains=value)
        )
