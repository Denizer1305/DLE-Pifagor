from __future__ import annotations

from apps.testing.models import TestAttemptIntegrityReport
from django.contrib import admin


@admin.register(TestAttemptIntegrityReport)
class TestAttemptIntegrityReportAdmin(admin.ModelAdmin):
    """
    Админка отчётов добросовестности прохождения теста.
    """

    list_display = (
        "id",
        "attempt",
        "get_test",
        "get_learner",
        "score",
        "risk_level",
        "checked_at",
        "updated_at",
    )
    list_filter = (
        "risk_level",
        "checked_at",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "attempt__test__title",
        "attempt__learner__email",
    )
    autocomplete_fields = ("attempt",)
    readonly_fields = (
        "checked_at",
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            "Связь",
            {"fields": ("attempt",)},
        ),
        (
            "Риск",
            {
                "fields": (
                    "score",
                    "risk_level",
                    "flags_data",
                )
            },
        ),
        (
            "Служебные даты",
            {
                "fields": (
                    "checked_at",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

    @admin.display(description="Тест")
    def get_test(self, obj):
        """
        Возвращает тест попытки.
        """

        return obj.attempt.test

    @admin.display(description="Обучающийся")
    def get_learner(self, obj):
        """
        Возвращает обучающегося попытки.
        """

        return obj.attempt.learner
