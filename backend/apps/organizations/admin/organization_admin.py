from __future__ import annotations

from apps.organizations.models import Organization
from django.contrib import admin


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    """
    Административная панель образовательных организаций.

    Позволяет управлять организациями, к которым привязываются:
        - пользователи;
        - роли;
        - преподаватели;
        - учащиеся;
        - группы;
        - заявки;
        - коды приглашения.
    """

    list_display = (
        "id",
        "name",
        "short_name",
        "code",
        "is_active",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "is_active",
        "created_at",
    )
    search_fields = (
        "name",
        "short_name",
        "code",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = ("name",)
