from __future__ import annotations

from apps.education.models import Curriculum, CurriculumItem
from apps.education.services import deactivate_curriculum_item


def deactivate_items_for_archived_curricula() -> dict[str, int]:
    """
    Деактивирует элементы архивных или неактивных учебных планов.
    """

    items = CurriculumItem.objects.filter(
        is_active=True,
    ).filter(
        curriculum__status=Curriculum.StatusChoices.ARCHIVED,
    )

    updated_count = 0

    for item in items:
        deactivate_curriculum_item(curriculum_item=item)
        updated_count += 1

    inactive_curriculum_items = CurriculumItem.objects.filter(
        is_active=True,
        curriculum__is_active=False,
    )

    for item in inactive_curriculum_items:
        deactivate_curriculum_item(curriculum_item=item)
        updated_count += 1

    return {
        "updated": updated_count,
    }
