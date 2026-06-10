from __future__ import annotations

import django_filters
from apps.testing.constants import GRADE_SOURCE_CHOICES, LEARNER_RESULT_STATUS_CHOICES
from apps.testing.models import TestLearnerResult


class TestLearnerResultFilter(django_filters.FilterSet):
    """
    Фильтры итоговых результатов тестов.
    """

    test_id = django_filters.NumberFilter(field_name="test_id")
    learner_id = django_filters.NumberFilter(field_name="learner_id")
    last_attempt_id = django_filters.NumberFilter(
        field_name="last_attempt_id",
    )

    status = django_filters.ChoiceFilter(
        choices=LEARNER_RESULT_STATUS_CHOICES,
    )
    grade_source = django_filters.ChoiceFilter(
        choices=GRADE_SOURCE_CHOICES,
    )

    is_passed = django_filters.BooleanFilter()
    is_blocked = django_filters.BooleanFilter()
    is_visible_to_learner = django_filters.BooleanFilter()
    is_visible_to_guardian = django_filters.BooleanFilter()

    min_average_score = django_filters.NumberFilter(
        field_name="average_score",
        lookup_expr="gte",
    )
    max_average_score = django_filters.NumberFilter(
        field_name="average_score",
        lookup_expr="lte",
    )
    min_average_grade = django_filters.NumberFilter(
        field_name="average_grade",
        lookup_expr="gte",
    )
    max_average_grade = django_filters.NumberFilter(
        field_name="average_grade",
        lookup_expr="lte",
    )

    class Meta:
        model = TestLearnerResult
        fields = (
            "test_id",
            "learner_id",
            "last_attempt_id",
            "status",
            "grade_source",
            "is_passed",
            "is_blocked",
            "is_visible_to_learner",
            "is_visible_to_guardian",
            "min_average_score",
            "max_average_score",
            "min_average_grade",
            "max_average_grade",
        )
