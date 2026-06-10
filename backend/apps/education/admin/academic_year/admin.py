from __future__ import annotations

from apps.education.admin.academic_year.actions import (
    deactivate_academic_years_action,
    restore_academic_years_action,
    set_current_academic_year_action,
)
from apps.education.admin.academic_year.inlines import EducationPeriodInline
from apps.education.models import AcademicYear
from django.contrib import admin


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    """
    Админка учебных годов.
    """

    list_display = (
        "name",
        "start_date",
        "end_date",
        "is_current",
        "is_active",
        "periods_count",
        "curricula_count",
        "updated_at",
    )
    list_filter = (
        "is_current",
        "is_active",
        "start_date",
        "end_date",
    )
    search_fields = (
        "name",
        "description",
    )
    ordering = (
        "-start_date",
        "name",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    date_hierarchy = "start_date"
    inlines = (EducationPeriodInline,)
    actions = (
        set_current_academic_year_action,
        deactivate_academic_years_action,
        restore_academic_years_action,
    )

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": (
                    "name",
                    "description",
                )
            },
        ),
        (
            "Даты",
            {
                "fields": (
                    "start_date",
                    "end_date",
                )
            },
        ),
        (
            "Статусы",
            {
                "fields": (
                    "is_current",
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

    @admin.display(description="Периодов")
    def periods_count(self, obj: AcademicYear) -> int:
        """
        Возвращает количество периодов учебного года.
        """

        return obj.periods.count()

    @admin.display(description="Учебных планов")
    def curricula_count(self, obj: AcademicYear) -> int:
        """
        Возвращает количество учебных планов учебного года.
        """

        return obj.curricula.count()
