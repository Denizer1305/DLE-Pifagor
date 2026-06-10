from __future__ import annotations

from apps.materials.models import Material
from apps.materials.selectors import get_material_by_id
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def publish_material(
    *,
    material: Material,
) -> Material:
    """
    Публикует учебный материал.
    """

    material.status = Material.StatusChoices.PUBLISHED
    material.is_active = True

    if not material.published_at:
        material.published_at = timezone.now()

    material.full_clean()
    material.save(
        update_fields=[
            "status",
            "is_active",
            "published_at",
            "updated_at",
        ],
    )

    return material


@transaction.atomic
def publish_material_by_id(
    *,
    material_id: int,
) -> Material:
    """
    Публикует учебный материал по идентификатору.
    """

    material = get_material_by_id(material_id)

    return publish_material(material=material)


@transaction.atomic
def archive_material(
    *,
    material: Material,
) -> Material:
    """
    Архивирует учебный материал.
    """

    material.status = Material.StatusChoices.ARCHIVED
    material.is_active = False

    if not material.archived_at:
        material.archived_at = timezone.now()

    material.full_clean()
    material.save(
        update_fields=[
            "status",
            "is_active",
            "archived_at",
            "updated_at",
        ],
    )

    return material


@transaction.atomic
def archive_material_by_id(
    *,
    material_id: int,
) -> Material:
    """
    Архивирует учебный материал по идентификатору.
    """

    material = get_material_by_id(material_id)

    return archive_material(material=material)


@transaction.atomic
def restore_material(
    *,
    material: Material,
) -> Material:
    """
    Восстанавливает учебный материал в черновик.
    """

    material.status = Material.StatusChoices.DRAFT
    material.is_active = True
    material.archived_at = None

    material.full_clean()
    material.save(
        update_fields=[
            "status",
            "is_active",
            "archived_at",
            "updated_at",
        ],
    )

    return material


@transaction.atomic
def restore_material_by_id(
    *,
    material_id: int,
) -> Material:
    """
    Восстанавливает учебный материал по идентификатору.
    """

    material = get_material_by_id(material_id)

    return restore_material(material=material)
