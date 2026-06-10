from __future__ import annotations

from apps.education.admin.education_period.actions import (
    deactivate_education_periods_action,
    restore_education_periods_action,
    set_current_education_period_action,
)
from apps.education.models import EducationPeriod
from django.contrib import admin


@admin.register(EducationPeriod)
class EducationPeriodAdmin(admin.ModelAdmin):
    """
    Админка учебных периодов.
    """

    list_display = (
        "name",
        "code",
        "academic_year",
        "period_type",
        "sequence",
        "start_date",
        "end_date",
        "is_current",
        "is_active",
    )
    list_filter = (
        "period_type",
        "is_current",
        "is_active",
        "academic_year",
    )
    search_fields = (
        "name",
        "code",
        "description",
        "academic_year__name",
    )
    raw_id_fields = ("academic_year",)
    ordering = (
        "academic_year",
        "sequence",
        "start_date",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    date_hierarchy = "start_date"
    actions = (
        set_current_education_period_action,
        deactivate_education_periods_action,
        restore_education_periods_action,
    )

    fieldsets = (
        (
            "Учебный год",
            {"fields": ("academic_year",)},
        ),
        (
            "Основная информация",
            {
                "fields": (
                    "name",
                    "code",
                    "period_type",
                    "sequence",
                    "description",
                )
            },
        ),
        (
            "Даты",
            {
                "fields": (
                    "start_date",
                    "end_date",
                )
            },
        ),
        (
            "Статусы",
            {
                "fields": (
                    "is_current",
                    "is_active",
                )
            },
        ),
        (
            "Служебная информация",
            {
                "classes": ("collapse",),
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )
