from __future__ import annotations

from apps.organizations.models import TeacherOrganization
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(TeacherOrganization)
class TeacherOrganizationAdmin(admin.ModelAdmin):
    """
    Админка связей преподавателей с образовательными организациями.
    """

    list_display = (
        "teacher",
        "organization",
        "position",
        "employment_type",
        "is_primary",
        "is_active",
        "starts_at",
        "ends_at",
        "is_current",
        "created_at",
    )
    list_filter = (
        "employment_type",
        "is_primary",
        "is_active",
        "organization",
    )
    search_fields = (
        "teacher__email",
        "teacher__phone",
        "teacher__first_name",
        "teacher__last_name",
        "organization__name",
        "organization__short_name",
        "organization__code",
        "position",
    )
    autocomplete_fields = (
        "teacher",
        "organization",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "is_current",
    )
    ordering = (
        "teacher",
        "-is_primary",
        "organization",
    )
    fieldsets = (
        (
            _("Связь"),
            {
                "fields": (
                    "teacher",
                    "organization",
                )
            },
        ),
        (
            _("Работа преподавателя"),
            {
                "fields": (
                    "position",
                    "employment_type",
                    "is_primary",
                    "is_active",
                    "starts_at",
                    "ends_at",
                    "notes",
                )
            },
        ),
        (
            _("Служебная информация"),
            {
                "fields": (
                    "is_current",
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )