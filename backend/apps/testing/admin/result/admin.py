from __future__ import annotations

from apps.testing.admin.result.actions import (
    hide_results,
    publish_results,
    recalculate_results,
)
from apps.testing.models import TestLearnerResult
from django.contrib import admin


@admin.register(TestLearnerResult)
class TestLearnerResultAdmin(admin.ModelAdmin):
    """
    Админка итоговых результатов тестов.
    """

    list_display = (
        "id",
        "test",
        "learner",
        "status",
        "attempts_count",
        "confirmed_attempts_count",
        "average_grade",
        "best_grade",
        "is_passed",
        "is_blocked",
        "is_visible_to_learner",
        "updated_at",
    )
    list_filter = (
        "status",
        "grade_source",
        "is_passed",
        "is_blocked",
        "is_visible_to_learner",
        "is_visible_to_guardian",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "test__title",
        "learner__email",
    )
    autocomplete_fields = (
        "test",
        "learner",
        "last_attempt",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "Связи",
            {
                "fields": (
                    "test",
                    "learner",
                    "last_attempt",
                )
            },
        ),
        (
            "Статус",
            {
                "fields": (
                    "status",
                    "grade_source",
                    "is_passed",
                    "is_blocked",
                )
            },
        ),
        (
            "Попытки",
            {
                "fields": (
                    "attempts_count",
                    "confirmed_attempts_count",
                )
            },
        ),
        (
            "Средние и лучшие значения",
            {
                "fields": (
                    "average_score",
                    "average_grade",
                    "best_score",
                    "best_grade",
                )
            },
        ),
        (
            "Видимость",
            {
                "fields": (
                    "is_visible_to_learner",
                    "is_visible_to_guardian",
                )
            },
        ),
        (
            "Служебные даты",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    actions = (
        recalculate_results,
        publish_results,
        hide_results,
    )
