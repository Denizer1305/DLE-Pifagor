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
        "has_active_teacher_registration_code",
        "created_at",
    )
    list_filter = (
        "is_active",
        "is_public",
        "is_default_public",
        "city",
        "teacher_registration_code_is_active",
    )
    search_fields = (
        "name",
        "short_name",
        "code",
        "city",
        "email",
        "phone",
    )
    prepopulated_fields = {
        "slug": ("code",),
    }
    readonly_fields = (
        "created_at",
        "updated_at",
        "teacher_registration_code_hash",
        "has_active_teacher_registration_code",
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
            _("Код регистрации преподавателя"),
            {
                "fields": (
                    "teacher_registration_code_hash",
                    "teacher_registration_code_is_active",
                    "teacher_registration_code_expires_at",
                    "has_active_teacher_registration_code",
                ),
                "description": _(
                    "Открытое значение кода здесь не хранится. "
                    "Для генерации и смены кода позже будет отдельное действие."
                ),
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