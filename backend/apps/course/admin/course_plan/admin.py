from __future__ import annotations

from apps.course.admin.course_plan.actions import (
    approve_course_plans_action,
    archive_course_plans_action,
    review_course_plans_action,
)
from apps.course.admin.course_plan.inlines import CoursePlanImportInline
from apps.course.models import CoursePlan, CoursePlanImport
from django.contrib import admin


@admin.register(CoursePlan)
class CoursePlanAdmin(admin.ModelAdmin):
    """
    Админка КТП курса.
    """

    list_display = (
        "course",
        "discipline_name",
        "specialty_code",
        "semester_number",
        "total_hours",
        "status",
        "is_active",
        "updated_at",
    )
    list_filter = (
        "status",
        "is_active",
        "semester_number",
        "course__organization",
        "course__subject",
        "course__academic_year",
    )
    search_fields = (
        "course__title",
        "course__code",
        "discipline_name",
        "discipline_code",
        "specialty_code",
        "specialty_name",
        "teacher_name_snapshot",
        "organization_name_snapshot",
        "academic_year_label",
        "commission_name",
        "protocol_number",
        "approved_order_number",
        "notes",
    )
    raw_id_fields = ("course",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = (
        "course__organization_id",
        "course__subject_id",
        "-updated_at",
    )
    date_hierarchy = "created_at"
    actions = (
        review_course_plans_action,
        approve_course_plans_action,
        archive_course_plans_action,
    )
    inlines = (CoursePlanImportInline,)

    fieldsets = (
        (
            "Курс и дисциплина",
            {
                "fields": (
                    "course",
                    "discipline_name",
                    "discipline_code",
                    "specialty_code",
                    "specialty_name",
                )
            },
        ),
        (
            "Снимки данных",
            {
                "fields": (
                    "teacher_name_snapshot",
                    "organization_name_snapshot",
                    "academic_year_label",
                )
            },
        ),
        (
            "Семестр и часы",
            {
                "fields": (
                    "semester_number",
                    "total_hours",
                    "semester_hours",
                    "theory_hours",
                    "practice_hours",
                    "lab_hours",
                    "self_study_hours",
                    "consultation_hours",
                )
            },
        ),
        (
            "Утверждение",
            {
                "fields": (
                    "commission_name",
                    "protocol_number",
                    "protocol_date",
                    "approved_order_number",
                    "approved_order_date",
                )
            },
        ),
        (
            "Состояние",
            {
                "fields": (
                    "status",
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

    def get_queryset(self, request):
        """
        Оптимизирует queryset списка КТП.
        """

        return (
            super()
            .get_queryset(request)
            .select_related(
                "course",
                "course__organization",
                "course__subject",
                "course__academic_year",
                "course__period",
            )
        )


@admin.register(CoursePlanImport)
class CoursePlanImportAdmin(admin.ModelAdmin):
    """
    Админка импортов КТП.
    """

    list_display = (
        "course_plan",
        "original_filename",
        "status",
        "parser_version",
        "imported_by",
        "imported_at",
        "applied_at",
    )
    list_filter = (
        "status",
        "parser_version",
        "imported_at",
        "applied_at",
    )
    search_fields = (
        "course_plan__course__title",
        "course_plan__course__code",
        "original_filename",
        "file_hash",
        "parser_version",
        "imported_by__email",
        "imported_by__first_name",
        "imported_by__last_name",
    )
    raw_id_fields = (
        "course_plan",
        "imported_by",
    )
    readonly_fields = (
        "imported_at",
        "applied_at",
    )
    ordering = (
        "-imported_at",
        "-id",
    )
    date_hierarchy = "imported_at"

    fieldsets = (
        (
            "Импорт",
            {
                "fields": (
                    "course_plan",
                    "source_file",
                    "original_filename",
                    "file_hash",
                    "status",
                    "parser_version",
                )
            },
        ),
        (
            "Результат разбора",
            {
                "fields": (
                    "parsed_payload",
                    "errors",
                )
            },
        ),
        (
            "Пользователь и даты",
            {
                "fields": (
                    "imported_by",
                    "imported_at",
                    "applied_at",
                )
            },
        ),
    )

    def get_queryset(self, request):
        """
        Оптимизирует queryset списка импортов.
        """

        return (
            super()
            .get_queryset(request)
            .select_related(
                "course_plan",
                "course_plan__course",
                "imported_by",
            )
        )
