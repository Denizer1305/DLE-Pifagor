from __future__ import annotations

from apps.testing.admin.bank.actions import (
    archive_bank_items,
    publish_bank_items,
    restore_bank_items,
)
from apps.testing.models import QuestionBankItem, QuestionBankOption
from django.contrib import admin


class QuestionBankOptionInline(admin.TabularInline):
    """
    Inline вариантов ответа шаблона вопроса.
    """

    model = QuestionBankOption
    extra = 0
    fields = (
        "text",
        "order",
        "is_correct",
        "score",
        "feedback",
        "is_active",
    )
    ordering = (
        "order",
        "id",
    )


@admin.register(QuestionBankItem)
class QuestionBankItemAdmin(admin.ModelAdmin):
    """
    Админка банка тестовых заданий.
    """

    list_display = (
        "id",
        "title",
        "question_type",
        "check_mode",
        "difficulty",
        "visibility",
        "status",
        "organization",
        "subject",
        "owner_teacher",
        "is_active",
        "updated_at",
    )
    list_filter = (
        "question_type",
        "check_mode",
        "difficulty",
        "visibility",
        "status",
        "is_active",
        "organization",
        "subject",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "title",
        "text",
        "explanation",
        "owner_teacher__email",
    )
    autocomplete_fields = (
        "organization",
        "subject",
        "owner_teacher",
    )
    readonly_fields = (
        "published_at",
        "archived_at",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "Основное",
            {
                "fields": (
                    "title",
                    "text",
                    "explanation",
                    "question_type",
                    "check_mode",
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
            "Классификация",
            {
                "fields": (
                    "score",
                    "difficulty",
                    "tags_data",
                    "organization",
                    "subject",
                    "owner_teacher",
                )
            },
        ),
        (
            "Публикация",
            {
                "fields": (
                    "visibility",
                    "status",
                    "is_active",
                    "published_at",
                    "archived_at",
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
    inlines = (QuestionBankOptionInline,)
    actions = (
        publish_bank_items,
        archive_bank_items,
        restore_bank_items,
    )


@admin.register(QuestionBankOption)
class QuestionBankOptionAdmin(admin.ModelAdmin):
    """
    Админка вариантов шаблонов вопросов.
    """

    list_display = (
        "id",
        "bank_item",
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
        "bank_item__title",
        "bank_item__text",
    )
    autocomplete_fields = ("bank_item",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "Связь",
            {"fields": ("bank_item",)},
        ),
        (
            "Вариант ответа",
            {
                "fields": (
                    "text",
                    "order",
                    "is_correct",
                    "score",
                    "feedback",
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
