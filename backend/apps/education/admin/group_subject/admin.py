from __future__ import annotations

from apps.education.admin.group_subject.actions import (
    deactivate_group_subjects_action,
    restore_group_subjects_action,
)
from apps.education.admin.group_subject.inlines import TeacherGroupSubjectInline
from apps.education.models import GroupSubject
from django.contrib import admin


@admin.register(GroupSubject)
class GroupSubjectAdmin(admin.ModelAdmin):
    """
    Админка предметов учебных групп.
    """

    list_display = (
        "group",
        "subject",
        "academic_year",
        "period",
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
        "academic_year",
        "period",
        "group__organization",
        "group__department",
    )
    search_fields = (
        "group__name",
        "group__code",
        "subject__name",
        "subject__short_name",
        "subject__code",
        "academic_year__name",
        "period__name",
        "period__code",
        "notes",
    )
    raw_id_fields = (
        "group",
        "subject",
        "academic_year",
        "period",
        "curriculum_item",
    )
    ordering = (
        "group",
        "period__sequence",
        "subject",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    inlines = (TeacherGroupSubjectInline,)
    actions = (
        deactivate_group_subjects_action,
        restore_group_subjects_action,
    )

    fieldsets = (
        (
            "Связи",
            {
                "fields": (
                    "group",
                    "subject",
                    "academic_year",
                    "period",
                    "curriculum_item",
                )
            },
        ),
        (
            "Часы",
            {
                "fields": (
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
