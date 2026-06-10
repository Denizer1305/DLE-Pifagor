from __future__ import annotations

from apps.course.admin.course.actions import (
    archive_courses_action,
    publish_courses_action,
    restore_courses_action,
)
from apps.course.admin.course.inlines import (
    CourseAccessRuleInline,
    CourseEnrollmentInline,
    CourseGroupAccessInline,
    CourseLessonInline,
    CourseMaterialLinkInline,
    CoursePlanInline,
    CourseSectionInline,
)
from apps.course.models import Course
from django.contrib import admin


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Админка курсов.
    """

    list_display = (
        "title",
        "code",
        "course_type",
        "status",
        "visibility",
        "organization",
        "subject",
        "academic_year",
        "period",
        "owner_teacher",
        "is_template",
        "is_active",
        "updated_at",
    )
    list_filter = (
        "course_type",
        "origin",
        "status",
        "visibility",
        "is_template",
        "is_active",
        "organization",
        "subject",
        "academic_year",
        "period",
    )
    search_fields = (
        "title",
        "subtitle",
        "description",
        "code",
        "slug",
        "organization__name",
        "organization__short_name",
        "organization__code",
        "subject__name",
        "subject__short_name",
        "subject__code",
        "owner_teacher__email",
        "owner_teacher__first_name",
        "owner_teacher__last_name",
    )
    raw_id_fields = (
        "owner_teacher",
        "organization",
        "subject",
        "academic_year",
        "period",
    )
    readonly_fields = (
        "published_at",
        "archived_at",
        "created_at",
        "updated_at",
    )
    ordering = (
        "organization_id",
        "subject_id",
        "-updated_at",
        "title",
    )
    date_hierarchy = "created_at"
    actions = (
        publish_courses_action,
        archive_courses_action,
        restore_courses_action,
    )
    inlines = (
        CoursePlanInline,
        CourseSectionInline,
        CourseLessonInline,
        CourseMaterialLinkInline,
        CourseGroupAccessInline,
        CourseAccessRuleInline,
        CourseEnrollmentInline,
    )

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "code",
                    "slug",
                    "title",
                    "subtitle",
                    "description",
                    "cover_image",
                )
            },
        ),
        (
            "Классификация",
            {
                "fields": (
                    "course_type",
                    "origin",
                    "status",
                    "visibility",
                    "level",
                    "language",
                )
            },
        ),
        (
            "Связи",
            {
                "fields": (
                    "owner_teacher",
                    "organization",
                    "subject",
                    "academic_year",
                    "period",
                )
            },
        ),
        (
            "Доступ и сроки",
            {
                "fields": (
                    "allow_self_enrollment",
                    "enrollment_code",
                    "starts_at",
                    "ends_at",
                )
            },
        ),
        (
            "Состояние",
            {
                "fields": (
                    "is_template",
                    "is_active",
                    "published_at",
                    "archived_at",
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
        Оптимизирует queryset списка курсов.
        """

        return (
            super()
            .get_queryset(request)
            .select_related(
                "owner_teacher",
                "organization",
                "subject",
                "academic_year",
                "period",
            )
        )
