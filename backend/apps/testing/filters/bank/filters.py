from __future__ import annotations

import django_filters
from apps.testing.constants import (
    BANK_ITEM_DIFFICULTY_CHOICES,
    BANK_ITEM_STATUS_CHOICES,
    BANK_ITEM_VISIBILITY_CHOICES,
    QUESTION_CHECK_MODE_CHOICES,
    QUESTION_TYPE_CHOICES,
)
from apps.testing.models import QuestionBankItem, QuestionBankOption


class QuestionBankItemFilter(django_filters.FilterSet):
    """
    Фильтры шаблонов вопросов банка тестовых заданий.
    """

    search = django_filters.CharFilter(method="filter_search")

    organization_id = django_filters.NumberFilter(
        field_name="organization_id",
    )
    subject_id = django_filters.NumberFilter(
        field_name="subject_id",
    )
    owner_teacher_id = django_filters.NumberFilter(
        field_name="owner_teacher_id",
    )

    question_type = django_filters.ChoiceFilter(
        choices=QUESTION_TYPE_CHOICES,
    )
    check_mode = django_filters.ChoiceFilter(
        choices=QUESTION_CHECK_MODE_CHOICES,
    )
    difficulty = django_filters.ChoiceFilter(
        choices=BANK_ITEM_DIFFICULTY_CHOICES,
    )
    visibility = django_filters.ChoiceFilter(
        choices=BANK_ITEM_VISIBILITY_CHOICES,
    )
    status = django_filters.ChoiceFilter(
        choices=BANK_ITEM_STATUS_CHOICES,
    )

    is_active = django_filters.BooleanFilter()

    class Meta:
        model = QuestionBankItem
        fields = (
            "search",
            "organization_id",
            "subject_id",
            "owner_teacher_id",
            "question_type",
            "check_mode",
            "difficulty",
            "visibility",
            "status",
            "is_active",
        )

    def filter_search(self, queryset, name, value):
        """
        Фильтрует шаблоны по названию, тексту и пояснению.
        """

        return (
            queryset.filter(
                title__icontains=value,
            )
            | queryset.filter(
                text__icontains=value,
            )
            | queryset.filter(
                explanation__icontains=value,
            )
        )


class QuestionBankOptionFilter(django_filters.FilterSet):
    """
    Фильтры вариантов ответа шаблонов вопросов.
    """

    bank_item_id = django_filters.NumberFilter(
        field_name="bank_item_id",
    )
    is_correct = django_filters.BooleanFilter()
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = QuestionBankOption
        fields = (
            "bank_item_id",
            "is_correct",
            "is_active",
        )
