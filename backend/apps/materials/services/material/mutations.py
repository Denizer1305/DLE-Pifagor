from __future__ import annotations

from typing import Any

from apps.materials.models import Material
from apps.materials.selectors import get_material_by_id
from apps.materials.services.material.payloads import MATERIAL_MUTABLE_FIELDS
from apps.materials.services.material.validation import validate_material_can_be_saved
from django.db import transaction


@transaction.atomic
def create_material(
    *,
    data: dict[str, Any],
) -> Material:
    """
    Создаёт учебный материал.
    """

    material = Material()

    _apply_material_data(
        material=material,
        data=data,
    )

    validate_material_can_be_saved(material=material)

    material.full_clean()
    material.save()

    return material


@transaction.atomic
def update_material(
    *,
    material: Material,
    data: dict[str, Any],
) -> Material:
    """
    Обновляет учебный материал.
    """

    _apply_material_data(
        material=material,
        data=data,
    )

    validate_material_can_be_saved(material=material)

    material.full_clean()
    material.save()

    return material


@transaction.atomic
def update_material_by_id(
    *,
    material_id: int,
    data: dict[str, Any],
) -> Material:
    """
    Обновляет учебный материал по идентификатору.
    """

    material = get_material_by_id(material_id)

    return update_material(
        material=material,
        data=data,
    )


def _apply_material_data(
    *,
    material: Material,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к материалу.
    """

    for field_name in MATERIAL_MUTABLE_FIELDS:
        if field_name in data:
            setattr(material, field_name, data[field_name])
