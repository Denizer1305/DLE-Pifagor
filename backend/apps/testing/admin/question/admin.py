from __future__ import annotations

from apps.testing.models import TestQuestion, TestQuestionOption
from django.contrib import admin


@admin.register(TestQuestion)
class TestQuestionAdmin(admin.ModelAdmin):
    """
    Админка вопросов теста.
    """

    list_display = (
        "id",
        "test",
        "question_type",
        "check_mode",
        "order",
        "score",
        "is_required",
        "is_active",
        "updated_at",
    )
    list_filter = (
        "question_type",
        "check_mode",
        "is_required",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "title",
        "text",
        "explanation",
        "test__title",
    )
    autocomplete_fields = ("test",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "test",
                    "question_type",
                    "check_mode",
                    "title",
                    "text",
                    "explanation",
                )
            },
        ),
        (
            "Ожидаемые ответы",
            {
                "fields": (
                    "expected_text_answer",
                    "expected_number_answer",
                    "case_sensitive",
                )
            },
        ),
        (
            "Настройки",
            {
                "fields": (
                    "order",
                    "score",
                    "is_required",
                    "is_active",
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


@admin.register(TestQuestionOption)
class TestQuestionOptionAdmin(admin.ModelAdmin):
    """
    Админка вариантов ответа.
    """

    list_display = (
        "id",
        "question",
        "order",
        "is_correct",
        "score",
        "is_active",
        "updated_at",
    )
    list_filter = (
        "is_correct",
        "is_active",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "text",
        "feedback",
        "question__title",
        "question__text",
        "question__test__title",
    )
    autocomplete_fields = ("question",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "question",
                    "text",
                    "order",
                )
            },
        ),
        (
            "Проверка",
            {
                "fields": (
                    "is_correct",
                    "score",
                    "feedback",
                )
            },
        ),
        (
            "Состояние",
            {
                "fields": (
                    "is_active",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
