from __future__ import annotations

from apps.education.admin.teacher_group_subject.actions import (
    deactivate_teacher_group_subjects_action,
    restore_teacher_group_subjects_action,
    set_primary_teacher_group_subject_action,
)
from apps.education.models import TeacherGroupSubject
from django.contrib import admin


@admin.register(TeacherGroupSubject)
class TeacherGroupSubjectAdmin(admin.ModelAdmin):
    """
    Админка назначений преподавателей на предметы групп.
    """

    list_display = (
        "teacher",
        "group_subject",
        "role",
        "is_primary",
        "is_active",
        "planned_hours",
        "starts_at",
        "ends_at",
    )
    list_filter = (
        "role",
        "is_primary",
        "is_active",
        "group_subject__academic_year",
        "group_subject__period",
        "group_subject__group__organization",
        "group_subject__group__department",
    )
    search_fields = (
        "teacher__email",
        "teacher__first_name",
        "teacher__last_name",
        "group_subject__group__name",
        "group_subject__group__code",
        "group_subject__subject__name",
        "group_subject__subject__short_name",
        "group_subject__subject__code",
        "notes",
    )
    raw_id_fields = (
        "teacher",
        "group_subject",
    )
    ordering = (
        "group_subject",
        "-is_primary",
        "teacher",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    date_hierarchy = "starts_at"
    actions = (
        set_primary_teacher_group_subject_action,
        deactivate_teacher_group_subjects_action,
        restore_teacher_group_subjects_action,
    )

    fieldsets = (
        (
            "Связи",
            {
                "fields": (
                    "teacher",
                    "group_subject",
                )
            },
        ),
        (
            "Роль и нагрузка",
            {
                "fields": (
                    "role",
                    "is_primary",
                    "is_active",
                    "planned_hours",
                )
            },
        ),
        (
            "Период назначения",
            {
                "fields": (
                    "starts_at",
                    "ends_at",
                )
            },
        ),
        (
            "Примечания",
            {"fields": ("notes",)},
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
