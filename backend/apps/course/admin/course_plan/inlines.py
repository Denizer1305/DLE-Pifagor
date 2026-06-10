from __future__ import annotations

from apps.course.models import CoursePlanImport
from django.contrib import admin


class CoursePlanImportInline(admin.TabularInline):
    """
    Inline импортов КТП.
    """

    model = CoursePlanImport
    extra = 0
    show_change_link = True

    fields = (
        "original_filename",
        "status",
        "parser_version",
        "imported_by",
        "imported_at",
        "applied_at",
    )
    readonly_fields = (
        "imported_at",
        "applied_at",
    )
    raw_id_fields = ("imported_by",)
    ordering = (
        "-imported_at",
        "-id",
    )
