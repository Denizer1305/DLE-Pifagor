from __future__ import annotations

from apps.organizations.models import Organization
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """
    Админка образовательных организаций.
    """

    list_display = (
        "name",
        "short_name",
        "code",
        "city",
        "is_active",
        "is_public",
        "is_default_public",
        "created_at",
    )
    list_filter = (
        "is_active",
        "is_public",
        "is_default_public",
        "city",
    )
    search_fields = (
        "name",
        "short_name",
        "code",
        "city",
        "email",
    )
    prepopulated_fields = {
        "slug": ("code",),
    }
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
                    "slug",
                    "code",
                    "description",
                )
            },
        ),
        (
            _("Контакты"),
            {
                "fields": (
                    "city",
                    "address",
                    "phone",
                    "email",
                    "website",
                    "logo",
                )
            },
        ),
        (
            _("Публичность"),
            {
                "fields": (
                    "is_active",
                    "is_public",
                    "is_default_public",
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
