from __future__ import annotations

from apps.education.models import TeacherGroupSubject
from django.contrib import admin


class TeacherGroupSubjectInline(admin.TabularInline):
    """
    Inline назначений преподавателей на предмет группы.
    """

    model = TeacherGroupSubject
    extra = 0
    show_change_link = True
    raw_id_fields = ("teacher",)
    fields = (
        "teacher",
        "role",
        "is_primary",
        "is_active",
        "planned_hours",
        "starts_at",
        "ends_at",
    )
