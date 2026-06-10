from __future__ import annotations

from apps.education.admin.curriculum_item.actions import (
    deactivate_curriculum_items_action,
    restore_curriculum_items_action,
)
from apps.education.models import CurriculumItem
from django.contrib import admin


@admin.register(CurriculumItem)
class CurriculumItemAdmin(admin.ModelAdmin):
    """
    Админка элементов учебного плана.
    """

    list_display = (
        "curriculum",
        "subject",
        "period",
        "sequence",
        "planned_hours",
        "contact_hours",
        "independent_hours",
        "assessment_type",
        "is_required",
        "is_active",
    )
    list_filter = (
        "assessment_type",
        "is_required",
        "is_active",
        "curriculum__organization",
        "curriculum__department",
        "curriculum__academic_year",
        "period",
    )
    search_fields = (
        "curriculum__code",
        "curriculum__name",
        "period__name",
        "period__code",
        "subject__name",
        "subject__short_name",
        "subject__code",
        "notes",
    )
    raw_id_fields = (
        "curriculum",
        "period",
        "subject",
    )
    ordering = (
        "curriculum",
        "period__sequence",
        "sequence",
        "subject",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    actions = (
        deactivate_curriculum_items_action,
        restore_curriculum_items_action,
    )

    fieldsets = (
        (
            "Связи",
            {
                "fields": (
                    "curriculum",
                    "period",
                    "subject",
                )
            },
        ),
        (
            "Порядок и часы",
            {
                "fields": (
                    "sequence",
                    "planned_hours",
                    "contact_hours",
                    "independent_hours",
                )
            },
        ),
        (
            "Аттестация и статус",
            {
                "fields": (
                    "assessment_type",
                    "is_required",
                    "is_active",
                    "notes",
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
