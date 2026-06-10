from __future__ import annotations

import django_filters
from apps.testing.constants import QUESTION_CHECK_MODE_CHOICES, QUESTION_TYPE_CHOICES
from apps.testing.models import TestQuestion
from django.db.models import Q


class TestQuestionFilter(django_filters.FilterSet):
    """
    Фильтры вопросов теста.
    """

    search = django_filters.CharFilter(method="filter_search")

    test_id = django_filters.NumberFilter(field_name="test_id")
    question_type = django_filters.ChoiceFilter(
        choices=QUESTION_TYPE_CHOICES,
    )
    check_mode = django_filters.ChoiceFilter(
        choices=QUESTION_CHECK_MODE_CHOICES,
    )
    is_required = django_filters.BooleanFilter()
    is_active = django_filters.BooleanFilter()

    min_score = django_filters.NumberFilter(
        field_name="score",
        lookup_expr="gte",
    )
    max_score = django_filters.NumberFilter(
        field_name="score",
        lookup_expr="lte",
    )

    class Meta:
        model = TestQuestion
        fields = (
            "search",
            "test_id",
            "question_type",
            "check_mode",
            "is_required",
            "is_active",
            "min_score",
            "max_score",
        )

    def filter_search(self, queryset, name, value):
        """
        Ищет вопрос по названию, тексту и пояснению.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(title__icontains=value)
            | Q(text__icontains=value)
            | Q(explanation__icontains=value)
        )
