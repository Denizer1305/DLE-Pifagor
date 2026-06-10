from __future__ import annotations

import django_filters
from apps.testing.constants import (
    TEST_STATUS_CHOICES,
    TEST_VISIBILITY_CHOICES,
    TestStatus,
)
from apps.testing.models import Test
from django.db.models import Q


class TestFilter(django_filters.FilterSet):
    """
    Фильтры тестов.
    """

    search = django_filters.CharFilter(method="filter_search")

    course_id = django_filters.NumberFilter(field_name="course_id")
    lesson_id = django_filters.NumberFilter(field_name="lesson_id")
    lesson_block_id = django_filters.NumberFilter(
        field_name="lesson_block_id",
    )
    organization_id = django_filters.NumberFilter(
        field_name="organization_id",
    )
    subject_id = django_filters.NumberFilter(field_name="subject_id")
    owner_teacher_id = django_filters.NumberFilter(
        field_name="owner_teacher_id",
    )

    status = django_filters.ChoiceFilter(choices=TEST_STATUS_CHOICES)
    visibility = django_filters.ChoiceFilter(
        choices=TEST_VISIBILITY_CHOICES,
    )
    is_active = django_filters.BooleanFilter()

    published_only = django_filters.BooleanFilter(
        method="filter_published_only",
    )

    class Meta:
        model = Test
        fields = (
            "search",
            "course_id",
            "lesson_id",
            "lesson_block_id",
            "organization_id",
            "subject_id",
            "owner_teacher_id",
            "status",
            "visibility",
            "is_active",
            "published_only",
        )

    def filter_search(self, queryset, name, value):
        """
        Ищет тест по названию, описанию и инструкции.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(title__icontains=value)
            | Q(description__icontains=value)
            | Q(instructions__icontains=value)
        )

    def filter_published_only(self, queryset, name, value):
        """
        Возвращает только опубликованные активные тесты.
        """

        if not value:
            return queryset

        return queryset.filter(
            status=TestStatus.PUBLISHED,
            is_active=True,
        )
