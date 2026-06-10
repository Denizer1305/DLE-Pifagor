from __future__ import annotations

from apps.course.admin.course_access.actions import (
    archive_course_enrollments_action,
    archive_course_group_accesses_action,
    cancel_course_enrollments_action,
    complete_course_enrollments_action,
    deactivate_course_access_rules_action,
    hide_course_for_groups_action,
    restore_course_access_rules_action,
    show_course_for_groups_action,
    start_course_enrollments_action,
)
from apps.course.models import CourseAccessRule, CourseEnrollment, CourseGroupAccess
from django.contrib import admin


@admin.register(CourseGroupAccess)
class CourseGroupAccessAdmin(admin.ModelAdmin):
    """
    Админка доступов групп к курсам.
    """

    list_display = (
        "course",
        "group",
        "visibility",
        "auto_enroll",
        "is_active",
        "starts_at",
        "ends_at",
    )
    list_filter = (
        "visibility",
        "auto_enroll",
        "is_active",
        "course__organization",
        "course__subject",
    )
    search_fields = (
        "course__title",
        "course__code",
        "group__name",
        "group__code",
        "notes",
    )
    raw_id_fields = (
        "course",
        "group",
        "group_subject",
        "teacher_group_subject",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = (
        "course_id",
        "group_id",
    )
    actions = (
        show_course_for_groups_action,
        hide_course_for_groups_action,
        archive_course_group_accesses_action,
    )

    fieldsets = (
        (
            "Связи",
            {
                "fields": (
                    "course",
                    "group",
                    "group_subject",
                    "teacher_group_subject",
                )
            },
        ),
        (
            "Доступ",
            {
                "fields": (
                    "visibility",
                    "starts_at",
                    "ends_at",
                    "auto_enroll",
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
        Оптимизирует queryset.
        """

        return (
            super()
            .get_queryset(request)
            .select_related(
                "course",
                "group",
                "group_subject",
                "teacher_group_subject",
                "course__organization",
                "course__subject",
            )
        )


@admin.register(CourseAccessRule)
class CourseAccessRuleAdmin(admin.ModelAdmin):
    """
    Админка правил доступа к курсам.
    """

    list_display = (
        "course",
        "access_type",
        "learner",
        "organization",
        "access_code",
        "auto_enroll",
        "is_active",
        "starts_at",
        "ends_at",
    )
    list_filter = (
        "access_type",
        "auto_enroll",
        "is_active",
        "course__organization",
        "course__subject",
    )
    search_fields = (
        "course__title",
        "course__code",
        "learner__email",
        "learner__first_name",
        "learner__last_name",
        "organization__name",
        "organization__short_name",
        "organization__code",
        "access_code",
        "notes",
    )
    raw_id_fields = (
        "course",
        "learner",
        "organization",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = (
        "course_id",
        "access_type",
        "id",
    )
    actions = (
        deactivate_course_access_rules_action,
        restore_course_access_rules_action,
    )

    fieldsets = (
        (
            "Правило",
            {
                "fields": (
                    "course",
                    "access_type",
                    "learner",
                    "organization",
                    "access_code",
                )
            },
        ),
        (
            "Доступ",
            {
                "fields": (
                    "starts_at",
                    "ends_at",
                    "auto_enroll",
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
        Оптимизирует queryset.
        """

        return (
            super()
            .get_queryset(request)
            .select_related(
                "course",
                "learner",
                "organization",
                "course__organization",
                "course__subject",
            )
        )


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    """
    Админка записей на курс.
    """

    list_display = (
        "course",
        "learner",
        "status",
        "progress_percent",
        "enrolled_at",
        "started_at",
        "completed_at",
        "last_activity_at",
    )
    list_filter = (
        "status",
        "course__organization",
        "course__subject",
        "course__academic_year",
    )
    search_fields = (
        "course__title",
        "course__code",
        "learner__email",
        "learner__first_name",
        "learner__last_name",
    )
    raw_id_fields = (
        "course",
        "learner",
        "group_access",
        "access_rule",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = (
        "-last_activity_at",
        "-enrolled_at",
        "-id",
    )
    actions = (
        start_course_enrollments_action,
        complete_course_enrollments_action,
        cancel_course_enrollments_action,
        archive_course_enrollments_action,
    )

    fieldsets = (
        (
            "Запись",
            {
                "fields": (
                    "course",
                    "learner",
                    "group_access",
                    "access_rule",
                    "status",
                )
            },
        ),
        (
            "Прогресс и даты",
            {
                "fields": (
                    "progress_percent",
                    "enrolled_at",
                    "started_at",
                    "completed_at",
                    "last_activity_at",
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
        Оптимизирует queryset.
        """

        return (
            super()
            .get_queryset(request)
            .select_related(
                "course",
                "learner",
                "group_access",
                "access_rule",
                "course__organization",
                "course__subject",
            )
        )
