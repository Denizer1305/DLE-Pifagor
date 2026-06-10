from __future__ import annotations

from apps.testing.models import TestAttemptAnswer
from django.contrib import admin


@admin.register(TestAttemptAnswer)
class TestAttemptAnswerAdmin(admin.ModelAdmin):
    """
    Админка ответов на вопросы теста.
    """

    list_display = (
        "id",
        "attempt",
        "question",
        "selected_option",
        "is_correct",
        "auto_score",
        "final_score",
        "requires_manual_review",
        "updated_at",
    )
    list_filter = (
        "is_correct",
        "requires_manual_review",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "attempt__test__title",
        "attempt__learner__email",
        "question__text",
        "text_answer",
        "teacher_comment",
    )
    autocomplete_fields = (
        "attempt",
        "question",
        "selected_option",
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
                    "attempt",
                    "question",
                )
            },
        ),
        (
            "Ответ обучающегося",
            {
                "fields": (
                    "selected_option",
                    "selected_options_data",
                    "text_answer",
                    "number_answer",
                )
            },
        ),
        (
            "Проверка",
            {
                "fields": (
                    "is_correct",
                    "auto_score",
                    "teacher_score",
                    "final_score",
                    "requires_manual_review",
                    "teacher_comment",
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
