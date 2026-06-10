from __future__ import annotations

import django_filters
from apps.education.models import LearnerGroupEnrollment
from django.db.models import Q, QuerySet


class LearnerGroupEnrollmentFilter(django_filters.FilterSet):
    """
    Фильтры академических зачислений обучающихся.
    """

    search = django_filters.CharFilter(method="filter_search")

    learner_id = django_filters.NumberFilter(
        field_name="learner_id",
    )
    organization_id = django_filters.NumberFilter(
        field_name="group__organization_id",
    )
    department_id = django_filters.NumberFilter(
        field_name="group__department_id",
    )
    group_id = django_filters.NumberFilter(
        field_name="group_id",
    )
    academic_year_id = django_filters.NumberFilter(
        field_name="academic_year_id",
    )

    status = django_filters.ChoiceFilter(
        choices=LearnerGroupEnrollment.StatusChoices.choices,
    )
    is_primary = django_filters.BooleanFilter()
    has_journal_number = django_filters.BooleanFilter(
        method="filter_has_journal_number",
    )

    enrollment_date_from = django_filters.DateFilter(
        field_name="enrollment_date",
        lookup_expr="gte",
    )
    enrollment_date_to = django_filters.DateFilter(
        field_name="enrollment_date",
        lookup_expr="lte",
    )
    completion_date_from = django_filters.DateFilter(
        field_name="completion_date",
        lookup_expr="gte",
    )
    completion_date_to = django_filters.DateFilter(
        field_name="completion_date",
        lookup_expr="lte",
    )

    ordering = django_filters.OrderingFilter(
        fields=(
            ("learner__last_name", "learner"),
            ("group__name", "group"),
            ("group__organization__name", "organization"),
            ("group__department__name", "department"),
            ("academic_year__start_date", "academic_year_start_date"),
            ("enrollment_date", "enrollment_date"),
            ("completion_date", "completion_date"),
            ("status", "status"),
            ("journal_number", "journal_number"),
            ("created_at", "created_at"),
            ("updated_at", "updated_at"),
        ),
    )

    class Meta:
        model = LearnerGroupEnrollment
        fields = (
            "search",
            "learner_id",
            "organization_id",
            "department_id",
            "group_id",
            "academic_year_id",
            "status",
            "is_primary",
            "has_journal_number",
            "enrollment_date_from",
            "enrollment_date_to",
            "completion_date_from",
            "completion_date_to",
            "ordering",
        )

    def filter_search(
        self,
        queryset: QuerySet,
        name: str,
        value: str,
    ) -> QuerySet:
        """
        Ищет академическое зачисление.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(learner__email__icontains=value)
            | Q(learner__first_name__icontains=value)
            | Q(learner__last_name__icontains=value)
            | Q(group__name__icontains=value)
            | Q(group__code__icontains=value)
            | Q(group__organization__name__icontains=value)
            | Q(group__organization__short_name__icontains=value)
            | Q(group__department__name__icontains=value)
            | Q(group__department__short_name__icontains=value)
            | Q(academic_year__name__icontains=value)
            | Q(notes__icontains=value)
        )

    def filter_has_journal_number(
        self,
        queryset: QuerySet,
        name: str,
        value: bool,
    ) -> QuerySet:
        """
        Фильтрует зачисления по наличию номера в журнале.
        """

        if value:
            return queryset.filter(journal_number__isnull=False)

        return queryset.filter(journal_number__isnull=True)
