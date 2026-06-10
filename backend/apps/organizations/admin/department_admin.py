from __future__ import annotations

from apps.organizations.models import Department
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """
    Административная панель отделений образовательной организации.

    Отделение используется для группировки учебных групп,
    преподавателей и заведующих отделением.
    """

    list_display = (
        "id",
        "name",
        "short_name",
        "code",
        "organization",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "organization",
        "is_active",
        "created_at",
    )
    search_fields = (
        "name",
        "short_name",
        "code",
        "organization__name",
        "organization__short_name",
        "organization__code",
    )
    autocomplete_fields = ("organization",)
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = (
        "organization",
        "name",
    )
    fieldsets = (
        (
            _("Основная информация"),
            {
                "fields": (
                    "organization",
                    "name",
                    "short_name",
                    "code",
                    "description",
                )
            },
        ),
        (
            _("Состояние"),
            {"fields": ("is_active",)},
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
