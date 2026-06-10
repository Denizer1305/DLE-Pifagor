from __future__ import annotations

from apps.education.admin.curriculum.actions import (
    activate_curricula_action,
    archive_curricula_action,
    restore_curricula_action,
)
from apps.education.admin.curriculum.inlines import CurriculumItemInline
from apps.education.models import Curriculum
from django.contrib import admin


@admin.register(Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    """
    Админка учебных планов.
    """

    list_display = (
        "code",
        "name",
        "organization",
        "department",
        "academic_year",
        "status",
        "is_active",
        "total_hours",
        "calculated_total_hours",
        "updated_at",
    )
    list_filter = (
        "status",
        "is_active",
        "organization",
        "department",
        "academic_year",
    )
    search_fields = (
        "code",
        "name",
        "description",
        "organization__name",
        "organization__short_name",
        "organization__code",
        "department__name",
        "department__short_name",
        "department__code",
        "academic_year__name",
    )
    raw_id_fields = (
        "organization",
        "department",
        "academic_year",
    )
    ordering = (
        "organization",
        "-academic_year__start_date",
        "name",
    )
    readonly_fields = (
        "calculated_total_hours",
        "created_at",
        "updated_at",
    )
    inlines = (CurriculumItemInline,)
    actions = (
        activate_curricula_action,
        archive_curricula_action,
        restore_curricula_action,
    )

    fieldsets = (
        (
            "Связи",
            {
                "fields": (
                    "organization",
                    "department",
                    "academic_year",
                )
            },
        ),
        (
            "Основная информация",
            {
                "fields": (
                    "code",
                    "name",
                    "description",
                )
            },
        ),
        (
            "Часы",
            {
                "fields": (
                    "total_hours",
                    "calculated_total_hours",
                )
            },
        ),
        (
            "Статус",
            {
                "fields": (
                    "status",
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
