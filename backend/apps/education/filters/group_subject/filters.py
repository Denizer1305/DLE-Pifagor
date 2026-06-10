from __future__ import annotations

import django_filters
from apps.education.models import GroupSubject
from django.db.models import Q, QuerySet


class GroupSubjectFilter(django_filters.FilterSet):
    """
    Фильтры предметов учебных групп.
    """

    search = django_filters.CharFilter(method="filter_search")

    organization_id = django_filters.NumberFilter(
        field_name="group__organization_id",
    )
    department_id = django_filters.NumberFilter(
        field_name="group__department_id",
    )
    group_id = django_filters.NumberFilter(
        field_name="group_id",
    )
    subject_id = django_filters.NumberFilter(
        field_name="subject_id",
    )
    academic_year_id = django_filters.NumberFilter(
        field_name="academic_year_id",
    )
    period_id = django_filters.NumberFilter(
        field_name="period_id",
    )
    curriculum_item_id = django_filters.NumberFilter(
        field_name="curriculum_item_id",
    )

    assessment_type = django_filters.ChoiceFilter(
        choices=GroupSubject.AssessmentTypeChoices.choices,
    )
    is_required = django_filters.BooleanFilter()
    is_active = django_filters.BooleanFilter()

    planned_hours_from = django_filters.NumberFilter(
        field_name="planned_hours",
        lookup_expr="gte",
    )
    planned_hours_to = django_filters.NumberFilter(
        field_name="planned_hours",
        lookup_expr="lte",
    )
    contact_hours_from = django_filters.NumberFilter(
        field_name="contact_hours",
        lookup_expr="gte",
    )
    contact_hours_to = django_filters.NumberFilter(
        field_name="contact_hours",
        lookup_expr="lte",
    )
    independent_hours_from = django_filters.NumberFilter(
        field_name="independent_hours",
        lookup_expr="gte",
    )
    independent_hours_to = django_filters.NumberFilter(
        field_name="independent_hours",
        lookup_expr="lte",
    )

    ordering = django_filters.OrderingFilter(
        fields=(
            ("group__name", "group"),
            ("group__organization__name", "organization"),
            ("group__department__name", "department"),
            ("subject__name", "subject"),
            ("academic_year__start_date", "academic_year_start_date"),
            ("period__sequence", "period_sequence"),
            ("planned_hours", "planned_hours"),
            ("contact_hours", "contact_hours"),
            ("independent_hours", "independent_hours"),
            ("created_at", "created_at"),
            ("updated_at", "updated_at"),
        ),
    )

    class Meta:
        model = GroupSubject
        fields = (
            "search",
            "organization_id",
            "department_id",
            "group_id",
            "subject_id",
            "academic_year_id",
            "period_id",
            "curriculum_item_id",
            "assessment_type",
            "is_required",
            "is_active",
            "planned_hours_from",
            "planned_hours_to",
            "contact_hours_from",
            "contact_hours_to",
            "independent_hours_from",
            "independent_hours_to",
            "ordering",
        )

    def filter_search(
        self,
        queryset: QuerySet,
        name: str,
        value: str,
    ) -> QuerySet:
        """
        Ищет предмет группы.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(group__name__icontains=value)
            | Q(group__code__icontains=value)
            | Q(group__organization__name__icontains=value)
            | Q(group__organization__short_name__icontains=value)
            | Q(group__department__name__icontains=value)
            | Q(group__department__short_name__icontains=value)
            | Q(subject__name__icontains=value)
            | Q(subject__short_name__icontains=value)
            | Q(subject__code__icontains=value)
            | Q(academic_year__name__icontains=value)
            | Q(period__name__icontains=value)
            | Q(period__code__icontains=value)
            | Q(notes__icontains=value)
        )
