from __future__ import annotations

import django_filters
from apps.testing.constants import INTEGRITY_RISK_LEVEL_CHOICES
from apps.testing.models import TestAttemptIntegrityReport


class TestAttemptIntegrityReportFilter(django_filters.FilterSet):
    """
    Фильтры отчётов добросовестности прохождения теста.
    """

    attempt_id = django_filters.NumberFilter(
        field_name="attempt_id",
    )
    test_id = django_filters.NumberFilter(
        field_name="attempt__test_id",
    )
    learner_id = django_filters.NumberFilter(
        field_name="attempt__learner_id",
    )

    risk_level = django_filters.ChoiceFilter(
        choices=INTEGRITY_RISK_LEVEL_CHOICES,
    )

    min_score = django_filters.NumberFilter(
        field_name="score",
        lookup_expr="gte",
    )
    max_score = django_filters.NumberFilter(
        field_name="score",
        lookup_expr="lte",
    )

    class Meta:
        model = TestAttemptIntegrityReport
        fields = (
            "attempt_id",
            "test_id",
            "learner_id",
            "risk_level",
            "min_score",
            "max_score",
        )
