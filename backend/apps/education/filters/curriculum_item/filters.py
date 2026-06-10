from __future__ import annotations

import django_filters
from apps.education.models import CurriculumItem
from django.db.models import Q, QuerySet


class CurriculumItemFilter(django_filters.FilterSet):
    """
    Фильтры элементов учебного плана.
    """

    search = django_filters.CharFilter(method="filter_search")

    curriculum_id = django_filters.NumberFilter(
        field_name="curriculum_id",
    )
    organization_id = django_filters.NumberFilter(
        field_name="curriculum__organization_id",
    )
    department_id = django_filters.NumberFilter(
        field_name="curriculum__department_id",
    )
    academic_year_id = django_filters.NumberFilter(
        field_name="curriculum__academic_year_id",
    )
    period_id = django_filters.NumberFilter(
        field_name="period_id",
    )
    subject_id = django_filters.NumberFilter(
        field_name="subject_id",
    )

    assessment_type = django_filters.ChoiceFilter(
        choices=CurriculumItem.AssessmentTypeChoices.choices,
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
            ("curriculum__name", "curriculum"),
            ("period__sequence", "period_sequence"),
            ("sequence", "sequence"),
            ("subject__name", "subject"),
            ("planned_hours", "planned_hours"),
            ("contact_hours", "contact_hours"),
            ("independent_hours", "independent_hours"),
            ("assessment_type", "assessment_type"),
            ("created_at", "created_at"),
            ("updated_at", "updated_at"),
        ),
    )

    class Meta:
        model = CurriculumItem
        fields = (
            "search",
            "curriculum_id",
            "organization_id",
            "department_id",
            "academic_year_id",
            "period_id",
            "subject_id",
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
        Ищет элемент учебного плана.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(curriculum__name__icontains=value)
            | Q(curriculum__code__icontains=value)
            | Q(subject__name__icontains=value)
            | Q(subject__short_name__icontains=value)
            | Q(subject__code__icontains=value)
            | Q(period__name__icontains=value)
            | Q(period__code__icontains=value)
            | Q(notes__icontains=value)
        )
