from __future__ import annotations

from typing import Any

from apps.materials.models import Material, MaterialVersion
from apps.materials.selectors import (
    get_material_version_by_id,
    get_next_material_version_number,
)
from apps.materials.services.material_version.current import (
    _unset_current_material_versions,
)
from apps.materials.services.material_version.payloads import (
    MATERIAL_VERSION_CREATE_FIELDS,
    MATERIAL_VERSION_UPDATE_FIELDS,
)
from apps.materials.services.material_version.validation import (
    validate_material_version_can_be_saved,
)
from django.db import transaction


@transaction.atomic
def create_material_version(
    *,
    data: dict[str, Any],
) -> MaterialVersion:
    """
    Создаёт версию учебного материала.
    """

    version = MaterialVersion()

    _apply_material_version_data(
        version=version,
        data=data,
        allowed_fields=MATERIAL_VERSION_CREATE_FIELDS,
    )

    if not version.version_number and version.material_id:
        version.version_number = get_next_material_version_number(
            version.material_id,
        )

    should_be_current = _material_version_should_be_current(version=version)

    if should_be_current:
        _unset_current_material_versions(
            material_id=version.material_id,
            exclude_id=None,
        )

    validate_material_version_can_be_saved(version=version)

    version.full_clean()
    version.save()

    if version.is_current:
        Material.objects.filter(id=version.material_id).update(
            current_version=version,
        )

    return version


@transaction.atomic
def update_material_version(
    *,
    version: MaterialVersion,
    data: dict[str, Any],
) -> MaterialVersion:
    """
    Обновляет версию учебного материала.
    """

    _apply_material_version_data(
        version=version,
        data=data,
        allowed_fields=MATERIAL_VERSION_UPDATE_FIELDS,
    )

    should_be_current = _material_version_should_be_current(version=version)

    if should_be_current:
        _unset_current_material_versions(
            material_id=version.material_id,
            exclude_id=version.id,
        )

    validate_material_version_can_be_saved(version=version)

    version.full_clean()
    version.save()

    if version.is_current:
        Material.objects.filter(id=version.material_id).update(
            current_version=version,
        )
    else:
        Material.objects.filter(
            id=version.material_id,
            current_version_id=version.id,
        ).update(current_version=None)

    return version


@transaction.atomic
def update_material_version_by_id(
    *,
    version_id: int,
    data: dict[str, Any],
) -> MaterialVersion:
    """
    Обновляет версию учебного материала по идентификатору.
    """

    version = get_material_version_by_id(version_id)

    return update_material_version(
        version=version,
        data=data,
    )


@transaction.atomic
def archive_material_version(
    *,
    version: MaterialVersion,
) -> MaterialVersion:
    """
    Архивирует версию учебного материала.
    """

    version.status = MaterialVersion.StatusChoices.ARCHIVED
    version.is_current = False
    version.full_clean()
    version.save(
        update_fields=[
            "status",
            "is_current",
            "updated_at",
        ],
    )

    Material.objects.filter(
        id=version.material_id,
        current_version_id=version.id,
    ).update(current_version=None)

    return version


@transaction.atomic
def archive_material_version_by_id(
    *,
    version_id: int,
) -> MaterialVersion:
    """
    Архивирует версию учебного материала по идентификатору.
    """

    version = get_material_version_by_id(version_id)

    return archive_material_version(version=version)


def _apply_material_version_data(
    *,
    version: MaterialVersion,
    data: dict[str, Any],
    allowed_fields: set[str],
) -> None:
    """
    Применяет входные данные к версии материала.
    """

    for field_name in allowed_fields:
        if field_name in data:
            setattr(version, field_name, data[field_name])


def _material_version_should_be_current(
    *,
    version: MaterialVersion,
) -> bool:
    """
    Проверяет, должна ли версия стать текущей.
    """

    return bool(
        version.is_current or version.status == MaterialVersion.StatusChoices.CURRENT
    )
