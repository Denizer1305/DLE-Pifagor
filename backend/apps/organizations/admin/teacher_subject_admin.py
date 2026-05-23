from __future__ import annotations

from apps.organizations.models import TeacherSubject
from django.contrib import admin


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
    )
    list_filter = (
        "is_primary",
        "is_active",
        "subject",
    )
    search_fields = (
        "teacher__email",
        "teacher__profile__first_name",
        "teacher__profile__last_name",
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
