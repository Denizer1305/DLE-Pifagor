from __future__ import annotations

from apps.organizations.models import TeacherSubject
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(TeacherSubject)
class TeacherSubjectAdmin(admin.ModelAdmin):
    """
    Админка связей преподавателей с предметами.
    """

    list_display = (
        "teacher",
        "subject",
        "is_primary",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "is_primary",
        "is_active",
        "subject",
    )
    search_fields = (
        "teacher__email",
        "teacher__phone",
        "teacher__first_name",
        "teacher__last_name",
        "subject__name",
        "subject__short_name",
        "subject__code",
    )
    autocomplete_fields = (
        "teacher",
        "subject",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = (
        "teacher",
        "-is_primary",
        "subject",
    )
    fieldsets = (
        (
            _("Связь"),
            {
                "fields": (
                    "teacher",
                    "subject",
                )
            },
        ),
        (
            _("Параметры"),
            {
                "fields": (
                    "is_primary",
                    "is_active",
                    "notes",
                )
            },
        ),
        (
            _("Служебная информация"),
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )
