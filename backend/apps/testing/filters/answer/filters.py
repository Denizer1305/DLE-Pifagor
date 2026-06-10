from __future__ import annotations

import django_filters
from apps.testing.models import TestAttemptAnswer
from django.db.models import Q


class TestAttemptAnswerFilter(django_filters.FilterSet):
    """
    Фильтры ответов на вопросы теста.
    """

    search = django_filters.CharFilter(method="filter_search")

    attempt_id = django_filters.NumberFilter(field_name="attempt_id")
    question_id = django_filters.NumberFilter(field_name="question_id")
    selected_option_id = django_filters.NumberFilter(
        field_name="selected_option_id",
    )

    is_correct = django_filters.BooleanFilter()
    requires_manual_review = django_filters.BooleanFilter()

    min_auto_score = django_filters.NumberFilter(
        field_name="auto_score",
        lookup_expr="gte",
    )
    max_auto_score = django_filters.NumberFilter(
        field_name="auto_score",
        lookup_expr="lte",
    )
    min_final_score = django_filters.NumberFilter(
        field_name="final_score",
        lookup_expr="gte",
    )
    max_final_score = django_filters.NumberFilter(
        field_name="final_score",
        lookup_expr="lte",
    )

    class Meta:
        model = TestAttemptAnswer
        fields = (
            "search",
            "attempt_id",
            "question_id",
            "selected_option_id",
            "is_correct",
            "requires_manual_review",
            "min_auto_score",
            "max_auto_score",
            "min_final_score",
            "max_final_score",
        )

    def filter_search(self, queryset, name, value):
        """
        Ищет ответ по текстовому ответу и комментарию преподавателя.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(text_answer__icontains=value) | Q(teacher_comment__icontains=value)
        )
