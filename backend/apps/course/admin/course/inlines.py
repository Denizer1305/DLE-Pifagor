from __future__ import annotations

from apps.course.models import (
    CourseAccessRule,
    CourseEnrollment,
    CourseGroupAccess,
    CourseLesson,
    CourseMaterialLink,
    CoursePlan,
    CourseSection,
)
from django.contrib import admin


class CoursePlanInline(admin.StackedInline):
    """
    Inline КТП курса.
    """

    model = CoursePlan
    extra = 0
    show_change_link = True

    fields = (
        "discipline_name",
        "discipline_code",
        "specialty_code",
        "specialty_name",
        "semester_number",
        "total_hours",
        "status",
        "is_active",
    )
    readonly_fields = ()


class CourseSectionInline(admin.TabularInline):
    """
    Inline разделов курса.
    """

    model = CourseSection
    extra = 0
    show_change_link = True

    fields = (
        "title",
        "section_number",
        "order",
        "planned_hours",
        "is_required",
        "is_published",
        "is_active",
    )
    ordering = (
        "order",
        "section_number",
        "id",
    )


class CourseLessonInline(admin.TabularInline):
    """
    Inline уроков курса.
    """

    model = CourseLesson
    extra = 0
    show_change_link = True

    fields = (
        "section",
        "lesson_number",
        "lesson_type",
        "title",
        "planned_hours",
        "order",
        "is_published",
        "is_active",
    )
    raw_id_fields = ("section",)
    ordering = (
        "section_id",
        "order",
        "lesson_number",
        "id",
    )


class CourseGroupAccessInline(admin.TabularInline):
    """
    Inline доступов групп к курсу.
    """

    model = CourseGroupAccess
    extra = 0
    show_change_link = True

    fields = (
        "group",
        "group_subject",
        "teacher_group_subject",
        "visibility",
        "auto_enroll",
        "is_active",
    )
    raw_id_fields = (
        "group",
        "group_subject",
        "teacher_group_subject",
    )


class CourseAccessRuleInline(admin.TabularInline):
    """
    Inline правил доступа к курсу.
    """

    model = CourseAccessRule
    extra = 0
    show_change_link = True

    fields = (
        "access_type",
        "learner",
        "organization",
        "access_code",
        "auto_enroll",
        "is_active",
    )
    raw_id_fields = (
        "learner",
        "organization",
    )


class CourseEnrollmentInline(admin.TabularInline):
    """
    Inline записей на курс.
    """

    model = CourseEnrollment
    extra = 0
    show_change_link = True

    fields = (
        "learner",
        "status",
        "progress_percent",
        "enrolled_at",
        "started_at",
        "completed_at",
    )
    raw_id_fields = (
        "learner",
        "group_access",
        "access_rule",
    )


class CourseMaterialLinkInline(admin.TabularInline):
    """
    Inline материалов курса.
    """

    model = CourseMaterialLink
    extra = 0
    show_change_link = True

    fields = (
        "section",
        "lesson",
        "material",
        "placement",
        "order",
        "is_required",
        "is_visible",
    )
    raw_id_fields = (
        "section",
        "lesson",
        "material",
    )
    ordering = (
        "section_id",
        "lesson_id",
        "order",
        "id",
    )
