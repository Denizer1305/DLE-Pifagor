from __future__ import annotations

from apps.testing.admin.test.actions import archive_tests, publish_tests, restore_tests
from apps.testing.models import Test
from django.contrib import admin


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    """
    Админка учебных тестов.
    """

    list_display = (
        "id",
        "title",
        "course",
        "owner_teacher",
        "status",
        "visibility",
        "max_attempts",
        "is_active",
        "published_at",
        "updated_at",
    )
    list_filter = (
        "status",
        "visibility",
        "is_active",
        "organization",
        "subject",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "title",
        "description",
        "instructions",
        "course__title",
        "owner_teacher__email",
    )
    autocomplete_fields = (
        "course",
        "lesson",
        "lesson_block",
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
                    "description",
                    "instructions",
                    "status",
                    "visibility",
                    "is_active",
                )
            },
        ),
        (
            "Привязка к обучению",
            {
                "fields": (
                    "course",
                    "lesson",
                    "lesson_block",
                    "organization",
                    "subject",
                    "owner_teacher",
                )
            },
        ),
        (
            "Настройки прохождения",
            {
                "fields": (
                    "max_attempts",
                    "time_limit_minutes",
                    "max_score",
                    "passing_score",
                    "shuffle_questions",
                    "shuffle_options",
                    "show_correct_answers_after_publish",
                )
            },
        ),
        (
            "Служебные даты",
            {
                "fields": (
                    "published_at",
                    "archived_at",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
    actions = (
        publish_tests,
        archive_tests,
        restore_tests,
    )
