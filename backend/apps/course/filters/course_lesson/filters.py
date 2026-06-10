from __future__ import annotations

import django_filters
from apps.course.models import CourseLesson
from django.db.models import Q


class CourseLessonFilter(django_filters.FilterSet):
    """
    Фильтры уроков курса.
    """

    search = django_filters.CharFilter(method="filter_search")

    course_id = django_filters.NumberFilter(field_name="course_id")
    section_id = django_filters.NumberFilter(field_name="section_id")

    lesson_type = django_filters.ChoiceFilter(
        field_name="lesson_type",
        choices=CourseLesson.LessonTypeChoices.choices,
    )

    is_required = django_filters.BooleanFilter(field_name="is_required")
    is_preview = django_filters.BooleanFilter(field_name="is_preview")
    is_published = django_filters.BooleanFilter(field_name="is_published")
    is_active = django_filters.BooleanFilter(field_name="is_active")

    planned_hours_min = django_filters.NumberFilter(
        field_name="planned_hours",
        lookup_expr="gte",
    )
    planned_hours_max = django_filters.NumberFilter(
        field_name="planned_hours",
        lookup_expr="lte",
    )

    available_after = django_filters.DateTimeFilter(
        field_name="available_from",
        lookup_expr="gte",
    )
    available_before = django_filters.DateTimeFilter(
        field_name="available_from",
        lookup_expr="lte",
    )

    class Meta:
        model = CourseLesson
        fields = (
            "search",
            "course_id",
            "section_id",
            "lesson_type",
            "is_required",
            "is_preview",
            "is_published",
            "is_active",
            "planned_hours_min",
            "planned_hours_max",
            "available_after",
            "available_before",
        )

    def filter_search(self, queryset, name: str, value: str):
        """
        Ищет урок по названию, содержанию, КТП-полям и курсу.
        """

        if not value:
            return queryset

        return queryset.filter(
            Q(title__icontains=value)
            | Q(short_content__icontains=value)
            | Q(visual_aids__icontains=value)
            | Q(literature__icontains=value)
            | Q(independent_work__icontains=value)
            | Q(notes__icontains=value)
            | Q(course__title__icontains=value)
            | Q(course__code__icontains=value)
            | Q(section__title__icontains=value)
        )
