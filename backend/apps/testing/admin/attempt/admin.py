from __future__ import annotations

from apps.testing.admin.attempt.actions import (
    auto_check_attempts,
    publish_attempt_results,
)
from apps.testing.models import TestAttempt
from django.contrib import admin


@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    """
    Админка попыток прохождения тестов.
    """

    list_display = (
        "id",
        "test",
        "learner",
        "attempt_number",
        "status",
        "check_status",
        "final_grade",
        "is_confirmed_by_teacher",
        "is_visible_to_learner",
        "expires_at",
        "updated_at",
    )
    list_filter = (
        "status",
        "check_status",
        "requires_manual_review",
        "is_confirmed_by_teacher",
        "is_visible_to_learner",
        "is_visible_to_guardian",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "test__title",
        "learner__email",
        "reviewer_teacher__email",
        "teacher_comment",
    )
    autocomplete_fields = (
        "test",
        "learner",
        "reviewer_teacher",
    )
    readonly_fields = (
        "started_at",
        "submitted_at",
        "auto_checked_at",
        "reviewed_at",
        "confirmed_at",
        "published_at",
        "created_at",
        "updated_at",
        "expires_at",
        "expired_at",
    )
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "test",
                    "learner",
                    "attempt_number",
                    "status",
                    "check_status",
                )
            },
        ),
        (
            "Баллы и оценки",
            {
                "fields": (
                    "auto_score",
                    "teacher_score",
                    "final_score",
                    "auto_grade",
                    "teacher_grade",
                    "final_grade",
                )
            },
        ),
        (
            "Проверка преподавателем",
            {
                "fields": (
                    "requires_manual_review",
                    "is_confirmed_by_teacher",
                    "reviewer_teacher",
                    "teacher_comment",
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
            "Даты",
            {
                "fields": (
                    "started_at",
                    "submitted_at",
                    "auto_checked_at",
                    "reviewed_at",
                    "confirmed_at",
                    "published_at",
                    "created_at",
                    "updated_at",
                    "expires_at",
                    "expired_at",
                )
            },
        ),
    )
    actions = (
        auto_check_attempts,
        publish_attempt_results,
    )
