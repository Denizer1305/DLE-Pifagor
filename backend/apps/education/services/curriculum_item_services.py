from __future__ import annotations

from typing import Any

from apps.education.models import CurriculumItem
from apps.education.selectors import get_curriculum_item_by_id
from django.db import transaction

CURRICULUM_ITEM_MUTABLE_FIELDS = {
    "curriculum",
    "curriculum_id",
    "period",
    "period_id",
    "subject",
    "subject_id",
    "sequence",
    "planned_hours",
    "contact_hours",
    "independent_hours",
    "assessment_type",
    "is_required",
    "is_active",
    "notes",
}


@transaction.atomic
def create_curriculum_item(*, data: dict[str, Any]) -> CurriculumItem:
    """
    Создаёт элемент учебного плана.
    """

    curriculum_item = CurriculumItem()

    _apply_curriculum_item_data(
        curriculum_item=curriculum_item,
        data=data,
    )

    curriculum_item.full_clean()
    curriculum_item.save()

    return curriculum_item


@transaction.atomic
def update_curriculum_item(
    *,
    curriculum_item: CurriculumItem,
    data: dict[str, Any],
) -> CurriculumItem:
    """
    Обновляет элемент учебного плана.
    """

    _apply_curriculum_item_data(
        curriculum_item=curriculum_item,
        data=data,
    )

    curriculum_item.full_clean()
    curriculum_item.save()

    return curriculum_item


@transaction.atomic
def update_curriculum_item_by_id(
    *,
    curriculum_item_id: int,
    data: dict[str, Any],
) -> CurriculumItem:
    """
    Обновляет элемент учебного плана по идентификатору.
    """

    curriculum_item = get_curriculum_item_by_id(curriculum_item_id)

    return update_curriculum_item(
        curriculum_item=curriculum_item,
        data=data,
    )


@transaction.atomic
def deactivate_curriculum_item(
    *,
    curriculum_item: CurriculumItem,
) -> CurriculumItem:
    """
    Деактивирует элемент учебного плана.
    """

    curriculum_item.is_active = False
    curriculum_item.full_clean()
    curriculum_item.save(
        update_fields=[
            "is_active",
            "updated_at",
        ],
    )

    return curriculum_item


@transaction.atomic
def deactivate_curriculum_item_by_id(
    *,
    curriculum_item_id: int,
) -> CurriculumItem:
    """
    Деактивирует элемент учебного плана по идентификатору.
    """

    curriculum_item = get_curriculum_item_by_id(curriculum_item_id)

    return deactivate_curriculum_item(curriculum_item=curriculum_item)


@transaction.atomic
def restore_curriculum_item(
    *,
    curriculum_item: CurriculumItem,
) -> CurriculumItem:
    """
    Восстанавливает элемент учебного плана.
    """

    curriculum_item.is_active = True
    curriculum_item.full_clean()
    curriculum_item.save(
        update_fields=[
            "is_active",
            "updated_at",
        ],
    )

    return curriculum_item


@transaction.atomic
def restore_curriculum_item_by_id(
    *,
    curriculum_item_id: int,
) -> CurriculumItem:
    """
    Восстанавливает элемент учебного плана по идентификатору.
    """

    curriculum_item = get_curriculum_item_by_id(curriculum_item_id)

    return restore_curriculum_item(curriculum_item=curriculum_item)


def _apply_curriculum_item_data(
    *,
    curriculum_item: CurriculumItem,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к элементу учебного плана.
    """

    for field_name in CURRICULUM_ITEM_MUTABLE_FIELDS:
        if field_name in data:
            setattr(curriculum_item, field_name, data[field_name])
