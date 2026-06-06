from __future__ import annotations

from apps.organizations.models import StudyGroup
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


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
        "course_number",
        "study_form",
        "status",
        "admission_year",
        "graduation_year",
        "is_active",
        "is_archived",
        "has_active_join_code",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "organization",
        "department",
        "study_form",
        "status",
        "is_active",
        "is_archived",
        "join_code_is_active",
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
        "join_code_hash",
        "has_active_join_code",
    )
    ordering = (
        "organization",
        "department",
        "name",
    )
    fieldsets = (
        (
            _("Основная информация"),
            {
                "fields": (
                    "organization",
                    "department",
                    "name",
                    "code",
                    "description",
                )
            },
        ),
        (
            _("Учебные данные"),
            {
                "fields": (
                    "admission_year",
                    "graduation_year",
                    "course_number",
                    "study_form",
                    "status",
                )
            },
        ),
        (
            _("Код вступления в группу"),
            {
                "fields": (
                    "join_code_hash",
                    "join_code_is_active",
                    "join_code_expires_at",
                    "has_active_join_code",
                ),
                "description": _(
                    "Открытое значение кода здесь не хранится. "
                    "Для генерации и смены кода позже будет отдельное действие."
                ),
            },
        ),
        (
            _("Состояние"),
            {
                "fields": (
                    "is_active",
                    "is_archived",
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