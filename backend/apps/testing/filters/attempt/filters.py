from __future__ import annotations

import django_filters
from apps.testing.constants import (
    ATTEMPT_CHECK_STATUS_CHOICES,
    TEST_ATTEMPT_STATUS_CHOICES,
)
from apps.testing.models import TestAttempt


class TestAttemptFilter(django_filters.FilterSet):
    """
    Фильтры попыток прохождения теста.
    """

    test_id = django_filters.NumberFilter(field_name="test_id")
    learner_id = django_filters.NumberFilter(field_name="learner_id")
    reviewer_teacher_id = django_filters.NumberFilter(
        field_name="reviewer_teacher_id",
    )

    status = django_filters.ChoiceFilter(
        choices=TEST_ATTEMPT_STATUS_CHOICES,
    )
    check_status = django_filters.ChoiceFilter(
        choices=ATTEMPT_CHECK_STATUS_CHOICES,
    )

    attempt_number = django_filters.NumberFilter()
    is_confirmed_by_teacher = django_filters.BooleanFilter()
    is_visible_to_learner = django_filters.BooleanFilter()
    is_visible_to_guardian = django_filters.BooleanFilter()
    requires_manual_review = django_filters.BooleanFilter()

    started_after = django_filters.DateTimeFilter(
        field_name="started_at",
        lookup_expr="gte",
    )
    started_before = django_filters.DateTimeFilter(
        field_name="started_at",
        lookup_expr="lte",
    )
    submitted_after = django_filters.DateTimeFilter(
        field_name="submitted_at",
        lookup_expr="gte",
    )
    submitted_before = django_filters.DateTimeFilter(
        field_name="submitted_at",
        lookup_expr="lte",
    )

    class Meta:
        model = TestAttempt
        fields = (
            "test_id",
            "learner_id",
            "reviewer_teacher_id",
            "status",
            "check_status",
            "attempt_number",
            "is_confirmed_by_teacher",
            "is_visible_to_learner",
            "is_visible_to_guardian",
            "requires_manual_review",
            "started_after",
            "started_before",
            "submitted_after",
            "submitted_before",
        )
