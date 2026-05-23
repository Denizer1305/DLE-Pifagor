from __future__ import annotations

from apps.organizations.models import Subject
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """
    Админка учебных предметов.
    """

    list_display = (
        "name",
        "short_name",
        "code",
        "is_active",
        "created_at",
    )
    list_filter = ("is_active",)
    search_fields = (
        "name",
        "short_name",
        "code",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    fieldsets = (
        (
            _("Основная информация"),
            {
                "fields": (
                    "name",
                    "short_name",
                    "code",
                    "description",
                )
            },
        ),
        (
            _("Статус"),
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
