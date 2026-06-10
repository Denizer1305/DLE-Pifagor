from __future__ import annotations

from datetime import date

from apps.education.models import Curriculum
from apps.education.services import archive_curriculum
from django.utils import timezone


def archive_curricula_for_finished_academic_years(
    *,
    reference_date: date | None = None,
) -> dict[str, int]:
    """
    Архивирует активные учебные планы завершённых учебных годов.
    """

    current_date = reference_date or timezone.localdate()

    curricula = Curriculum.objects.filter(
        is_active=True,
        academic_year__end_date__lt=current_date,
    ).exclude(
        status=Curriculum.StatusChoices.ARCHIVED,
    )

    updated_count = 0

    for curriculum in curricula:
        archive_curriculum(curriculum=curriculum)
        updated_count += 1

    return {
        "updated": updated_count,
    }
