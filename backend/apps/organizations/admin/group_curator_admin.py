from __future__ import annotations

from apps.organizations.models import GroupCurator
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(GroupCurator)
class GroupCuratorAdmin(admin.ModelAdmin):
    """
    Админка кураторов учебных групп.
    """

    list_display = (
        "group",
        "teacher",
        "is_primary",
        "is_active",
        "starts_at",
        "ends_at",
        "is_current",
        "created_at",
    )
    list_filter = (
        "is_primary",
        "is_active",
        "group__organization",
        "group__department",
    )
    search_fields = (
        "group__name",
        "group__code",
        "teacher__email",
        "teacher__phone",
        "teacher__first_name",
        "teacher__last_name",
    )
    autocomplete_fields = (
        "group",
        "teacher",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
        "is_current",
    )
    ordering = (
        "group",
        "-is_primary",
        "teacher",
    )
    fieldsets = (
        (
            _("Связь"),
            {
                "fields": (
                    "group",
                    "teacher",
                )
            },
        ),
        (
            _("Параметры кураторства"),
            {
                "fields": (
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