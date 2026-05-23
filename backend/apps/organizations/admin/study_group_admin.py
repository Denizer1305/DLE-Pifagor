from __future__ import annotations

from apps.organizations.models import StudyGroup
from django.contrib import admin


@admin.register(StudyGroup)
class StudyGroupAdmin(admin.ModelAdmin):
    """
    Административная панель учебных групп и классов.

    Учебная группа используется для прикрепления учащихся,
    кураторов, расписания, журнала и заявок.
    """

    list_display = (
        "id",
        "name",
        "code",
        "organization",
        "department",
        "admission_year",
        "graduation_year",
        "is_active",
        "is_archived",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "organization",
        "department",
        "is_active",
        "is_archived",
        "admission_year",
        "graduation_year",
        "created_at",
    )
    search_fields = (
        "name",
        "code",
        "organization__name",
        "organization__short_name",
        "organization__code",
        "department__name",
        "department__short_name",
        "department__code",
    )
    autocomplete_fields = (
        "organization",
        "department",
    )
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    ordering = (
        "organization",
        "department",
        "name",
    )
