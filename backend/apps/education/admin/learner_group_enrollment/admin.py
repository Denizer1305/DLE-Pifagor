from __future__ import annotations

from apps.education.admin.learner_group_enrollment.actions import (
    archive_learner_enrollments_action,
    set_primary_learner_enrollment_action,
)
from apps.education.models import LearnerGroupEnrollment
from django.contrib import admin


@admin.register(LearnerGroupEnrollment)
class LearnerGroupEnrollmentAdmin(admin.ModelAdmin):
    """
    Админка академических зачислений обучающихся.
    """

    list_display = (
        "learner",
        "group",
        "academic_year",
        "status",
        "is_primary",
        "journal_number",
        "enrollment_date",
        "completion_date",
    )
    list_filter = (
        "status",
        "is_primary",
        "academic_year",
        "group__organization",
        "group__department",
    )
    search_fields = (
        "learner__email",
        "learner__first_name",
        "learner__last_name",
        "group__name",
        "group__code",
        "academic_year__name",
        "notes",
    )
    raw_id_fields = (
        "learner",
        "group",
        "academic_year",
    )
    ordering = (
        "-academic_year__start_date",
        "group",
        "journal_number",
        "learner",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    date_hierarchy = "enrollment_date"
    actions = (
        set_primary_learner_enrollment_action,
        archive_learner_enrollments_action,
    )

    fieldsets = (
        (
            "Связи",
            {
                "fields": (
                    "learner",
                    "group",
                    "academic_year",
                )
            },
        ),
        (
            "Зачисление",
            {
                "fields": (
                    "enrollment_date",
                    "completion_date",
                    "status",
                    "is_primary",
                    "journal_number",
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
