from __future__ import annotations

from apps.education.models import CurriculumItem
from django.contrib import admin


class CurriculumItemInline(admin.TabularInline):
    """
    Inline элементов учебного плана.
    """

    model = CurriculumItem
    extra = 0
    show_change_link = True
    raw_id_fields = (
        "period",
        "subject",
    )
    fields = (
        "period",
        "subject",
        "sequence",
        "planned_hours",
        "contact_hours",
        "independent_hours",
        "assessment_type",
        "is_required",
        "is_active",
    )
