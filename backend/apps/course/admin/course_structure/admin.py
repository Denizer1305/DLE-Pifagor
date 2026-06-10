from __future__ import annotations

from apps.course.admin.course_structure.actions import (
    archive_course_lessons_action,
    archive_course_sections_action,
    hide_course_lesson_blocks_action,
    hide_course_material_links_action,
    publish_course_lessons_action,
    publish_course_sections_action,
    show_course_lesson_blocks_action,
    show_course_material_links_action,
)
from apps.course.models import (
    CourseLesson,
    CourseLessonBlock,
    CourseMaterialLink,
    CourseSection,
)
from django.contrib import admin


@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    """
    Админка разделов курса.
    """

    list_display = (
        "title",
        "course",
        "section_number",
        "order",
        "planned_hours",
        "is_required",
        "is_published",
        "is_active",
    )
    list_filter = (
        "is_required",
        "is_published",
        "is_active",
        "course__organization",
        "course__subject",
    )
    search_fields = (
        "title",
        "description",
        "course__title",
        "course__code",
    )
    raw_id_fields = ("course",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = (
        "course_id",
        "order",
        "section_number",
        "title",
    )
    actions = (
        publish_course_sections_action,
        archive_course_sections_action,
    )

    fieldsets = (
        (
            "Раздел",
            {
                "fields": (
                    "course",
                    "title",
                    "description",
                    "section_number",
                    "order",
                    "planned_hours",
                )
            },
        ),
        (
            "Состояние",
            {
                "fields": (
                    "is_required",
                    "is_published",
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

    def get_queryset(self, request):
        """
        Оптимизирует queryset.
        """

        return (
            super()
            .get_queryset(request)
            .select_related(
                "course",
                "course__organization",
                "course__subject",
            )
        )


@admin.register(CourseLesson)
class CourseLessonAdmin(admin.ModelAdmin):
    """
    Админка уроков курса.
    """

    list_display = (
        "title",
        "course",
        "section",
        "lesson_number",
        "lesson_type",
        "planned_hours",
        "order",
        "is_required",
        "is_preview",
        "is_published",
        "is_active",
    )
    list_filter = (
        "lesson_type",
        "is_required",
        "is_preview",
        "is_published",
        "is_active",
        "course__organization",
        "course__subject",
    )
    search_fields = (
        "title",
        "short_content",
        "visual_aids",
        "literature",
        "independent_work",
        "notes",
        "course__title",
        "course__code",
        "section__title",
    )
    raw_id_fields = (
        "course",
        "section",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = (
        "course_id",
        "section_id",
        "order",
        "lesson_number",
        "id",
    )
    actions = (
        publish_course_lessons_action,
        archive_course_lessons_action,
    )

    fieldsets = (
        (
            "Урок",
            {
                "fields": (
                    "course",
                    "section",
                    "lesson_number",
                    "lesson_type",
                    "title",
                    "short_content",
                    "order",
                )
            },
        ),
        (
            "Часы",
            {
                "fields": (
                    "planned_hours",
                    "theory_hours",
                    "practice_hours",
                    "lab_hours",
                    "self_study_hours",
                )
            },
        ),
        (
            "КТП-поля",
            {
                "fields": (
                    "visual_aids",
                    "literature",
                    "independent_work",
                    "notes",
                )
            },
        ),
        (
            "Доступность",
            {
                "fields": (
                    "available_from",
                    "is_required",
                    "is_preview",
                    "is_published",
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

    def get_queryset(self, request):
        """
        Оптимизирует queryset.
        """

        return (
            super()
            .get_queryset(request)
            .select_related(
                "course",
                "section",
                "course__organization",
                "course__subject",
            )
        )


@admin.register(CourseLessonBlock)
class CourseLessonBlockAdmin(admin.ModelAdmin):
    """
    Админка блоков урока.
    """

    list_display = (
        "title",
        "lesson",
        "block_type",
        "material",
        "order",
        "is_visible",
    )
    list_filter = (
        "block_type",
        "is_visible",
        "lesson__course__organization",
        "lesson__course__subject",
    )
    search_fields = (
        "title",
        "content",
        "external_url",
        "lesson__title",
        "material__title",
        "material__slug",
    )
    raw_id_fields = (
        "lesson",
        "material",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = (
        "lesson_id",
        "order",
        "id",
    )
    actions = (
        show_course_lesson_blocks_action,
        hide_course_lesson_blocks_action,
    )

    fieldsets = (
        (
            "Блок урока",
            {
                "fields": (
                    "lesson",
                    "block_type",
                    "title",
                    "content",
                    "external_url",
                    "material",
                    "order",
                    "is_visible",
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
                "lesson",
                "lesson__course",
                "material",
            )
        )


@admin.register(CourseMaterialLink)
class CourseMaterialLinkAdmin(admin.ModelAdmin):
    """
    Админка связей курса с материалами.
    """

    list_display = (
        "course",
        "section",
        "lesson",
        "material",
        "placement",
        "order",
        "is_required",
        "is_visible",
    )
    list_filter = (
        "placement",
        "is_required",
        "is_visible",
        "course__organization",
        "course__subject",
    )
    search_fields = (
        "course__title",
        "course__code",
        "section__title",
        "lesson__title",
        "material__title",
        "material__slug",
        "notes",
    )
    raw_id_fields = (
        "course",
        "section",
        "lesson",
        "material",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = (
        "course_id",
        "section_id",
        "lesson_id",
        "order",
        "id",
    )
    actions = (
        show_course_material_links_action,
        hide_course_material_links_action,
    )

    fieldsets = (
        (
            "Связь",
            {
                "fields": (
                    "course",
                    "section",
                    "lesson",
                    "material",
                    "placement",
                    "order",
                )
            },
        ),
        (
            "Настройки",
            {
                "fields": (
                    "is_required",
                    "is_visible",
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
                "section",
                "lesson",
                "material",
                "course__organization",
                "course__subject",
            )
        )
