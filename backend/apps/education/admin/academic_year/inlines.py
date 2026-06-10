from __future__ import annotations

from apps.education.models import EducationPeriod
from django.contrib import admin


class EducationPeriodInline(admin.TabularInline):
    """
    Inline учебных периодов внутри учебного года.
    """

    model = EducationPeriod
    extra = 0
    show_change_link = True

    fields = (
        "name",
        "code",
        "period_type",
        "sequence",
        "start_date",
        "end_date",
        "is_current",
        "is_active",
    )
    readonly_fields = ()
