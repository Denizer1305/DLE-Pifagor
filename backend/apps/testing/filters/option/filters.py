from __future__ import annotations

import django_filters
from apps.testing.models import TestQuestionOption
from django.db.models import Q


class TestQuestionOptionFilter(django_filters.FilterSet):
    """
    Фильтры вариантов ответа.
    """

    search = django_filters.CharFilter(method="filter_search")

    question_id = django_filters.NumberFilter(field_name="question_id")
    is_correct = django_filters.BooleanFilter()
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
        model = TestQuestionOption
        fields = (
            "search",
            "question_id",
            "is_correct",
            "is_active",
            "min_score",
            "max_score",
        )

    def filter_search(self, queryset, name, value):
        """
        Ищет вариант ответа по тексту и пояснению.
        """

        if not value:
            return queryset

        return queryset.filter(Q(text__icontains=value) | Q(feedback__icontains=value))
