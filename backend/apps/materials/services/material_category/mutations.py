from __future__ import annotations

from typing import Any

from apps.materials.models import MaterialCategory
from apps.materials.selectors import get_material_category_by_id
from apps.materials.services.material_category.payloads import (
    MATERIAL_CATEGORY_MUTABLE_FIELDS,
)
from apps.materials.services.material_category.validation import (
    validate_material_category_can_be_saved,
)
from django.db import transaction


@transaction.atomic
def create_material_category(
    *,
    data: dict[str, Any],
) -> MaterialCategory:
    """
    Создаёт категорию учебных материалов.
    """

    category = MaterialCategory()

    _apply_material_category_data(
        category=category,
        data=data,
    )

    validate_material_category_can_be_saved(category=category)

    category.full_clean()
    category.save()

    return category


@transaction.atomic
def update_material_category(
    *,
    category: MaterialCategory,
    data: dict[str, Any],
) -> MaterialCategory:
    """
    Обновляет категорию учебных материалов.
    """

    _apply_material_category_data(
        category=category,
        data=data,
    )

    validate_material_category_can_be_saved(category=category)

    category.full_clean()
    category.save()

    return category


@transaction.atomic
def update_material_category_by_id(
    *,
    category_id: int,
    data: dict[str, Any],
) -> MaterialCategory:
    """
    Обновляет категорию учебных материалов по идентификатору.
    """

    category = get_material_category_by_id(category_id)

    return update_material_category(
        category=category,
        data=data,
    )


@transaction.atomic
def deactivate_material_category(
    *,
    category: MaterialCategory,
) -> MaterialCategory:
    """
    Деактивирует категорию учебных материалов.
    """

    category.is_active = False
    category.full_clean()
    category.save(
        update_fields=[
            "is_active",
            "updated_at",
        ],
    )

    return category


@transaction.atomic
def deactivate_material_category_by_id(
    *,
    category_id: int,
) -> MaterialCategory:
    """
    Деактивирует категорию учебных материалов по идентификатору.
    """

    category = get_material_category_by_id(category_id)

    return deactivate_material_category(category=category)


@transaction.atomic
def restore_material_category(
    *,
    category: MaterialCategory,
) -> MaterialCategory:
    """
    Восстанавливает категорию учебных материалов.
    """

    category.is_active = True
    category.full_clean()
    category.save(
        update_fields=[
            "is_active",
            "updated_at",
        ],
    )

    return category


@transaction.atomic
def restore_material_category_by_id(
    *,
    category_id: int,
) -> MaterialCategory:
    """
    Восстанавливает категорию учебных материалов по идентификатору.
    """

    category = get_material_category_by_id(category_id)

    return restore_material_category(category=category)


def _apply_material_category_data(
    *,
    category: MaterialCategory,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к категории материала.
    """

    for field_name in MATERIAL_CATEGORY_MUTABLE_FIELDS:
        if field_name in data:
            setattr(category, field_name, data[field_name])
