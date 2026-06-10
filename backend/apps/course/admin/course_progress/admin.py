from __future__ import annotations

from apps.course.models import CourseProgress, LessonProgress
from django.contrib import admin


@admin.register(CourseProgress)
class CourseProgressAdmin(admin.ModelAdmin):
    """
    Админка общего прогресса курса.
    """

    list_display = (
        "enrollment",
        "progress_percent",
        "total_lessons_count",
        "completed_lessons_count",
        "last_lesson",
        "last_activity_at",
    )
    list_filter = (
        "last_activity_at",
        "enrollment__course__organization",
        "enrollment__course__subject",
    )
    search_fields = (
        "enrollment__course__title",
        "enrollment__course__code",
        "enrollment__learner__email",
        "enrollment__learner__first_name",
        "enrollment__learner__last_name",
        "last_lesson__title",
    )
    raw_id_fields = (
        "enrollment",
        "last_lesson",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = (
        "-last_activity_at",
        "-updated_at",
        "-id",
    )

    fieldsets = (
        (
            "Прогресс",
            {
                "fields": (
                    "enrollment",
                    "progress_percent",
                    "total_lessons_count",
                    "completed_lessons_count",
                    "last_lesson",
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
                "enrollment",
                "enrollment__course",
                "enrollment__learner",
                "last_lesson",
            )
        )


@admin.register(LessonProgress)
class LessonProgressAdmin(admin.ModelAdmin):
    """
    Админка прогресса уроков.
    """

    list_display = (
        "enrollment",
        "lesson",
        "status",
        "progress_percent_display",
        "started_at",
        "completed_at",
        "activity_at_display",
    )
    list_filter = (
        "status",
        "started_at",
        "completed_at",
        "updated_at",
        "enrollment__course__organization",
        "enrollment__course__subject",
    )
    search_fields = (
        "enrollment__course__title",
        "enrollment__course__code",
        "enrollment__learner__email",
        "enrollment__learner__first_name",
        "enrollment__learner__last_name",
        "lesson__title",
    )
    raw_id_fields = (
        "enrollment",
        "course_progress",
        "lesson",
    )
    readonly_fields = (
        "progress_percent_display",
        "activity_at_display",
        "created_at",
        "updated_at",
    )
    ordering = (
        "lesson__section_id",
        "lesson__order",
        "lesson__lesson_number",
        "id",
    )

    fieldsets = (
        (
            "Прогресс урока",
            {
                "fields": (
                    "enrollment",
                    "course_progress",
                    "lesson",
                    "status",
                    "progress_percent_display",
                )
            },
        ),
        (
            "Даты",
            {
                "fields": (
                    "started_at",
                    "completed_at",
                    "activity_at_display",
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

    @admin.display(description="Прогресс")
    def progress_percent_display(self, obj: LessonProgress) -> str:
        """
        Возвращает вычисляемый процент прогресса урока.
        """

        completed_status = getattr(
            LessonProgress.StatusChoices,
            "COMPLETED",
            "completed",
        )
        in_progress_status = getattr(
            LessonProgress.StatusChoices,
            "IN_PROGRESS",
            "in_progress",
        )

        if obj.status == completed_status:
            return "100%"

        if obj.status == in_progress_status:
            return "50%"

        return "0%"

    @admin.display(description="Последняя активность")
    def activity_at_display(self, obj: LessonProgress):
        """
        Возвращает дату последней активности по уроку.
        """

        return obj.completed_at or obj.started_at or obj.updated_at or obj.created_at

    def get_queryset(self, request):
        """
        Оптимизирует queryset.
        """

        return (
            super()
            .get_queryset(request)
            .select_related(
                "enrollment",
                "course_progress",
                "lesson",
                "lesson__section",
                "enrollment__course",
                "enrollment__learner",
            )
        )
