from __future__ import annotations

import hashlib
import mimetypes
from typing import Iterable

from apps.materials.models import Material, MaterialVersion
from apps.materials.services import set_current_material_version
from django.db import transaction


@transaction.atomic
def ensure_current_version_for_material(
    *,
    material_id: int,
) -> dict[str, int | bool]:
    """
    Гарантирует наличие текущей версии у материала.

    Если current_version уже корректен — ничего не меняет.
    Если есть версия с is_current=True — привязывает её к материалу.
    Если текущей версии нет — выбирает последнюю неархивную версию.
    """

    material = Material.objects.get(id=material_id)

    if (
        material.current_version_id
        and material.current_version.material_id == material.id
        and material.current_version.is_current
    ):
        return {
            "material_id": material.id,
            "changed": False,
            "current_version_id": material.current_version_id,
        }

    version = (
        MaterialVersion.objects.filter(
            material=material,
            is_current=True,
        )
        .exclude(status=MaterialVersion.StatusChoices.ARCHIVED)
        .order_by("-version_number", "-created_at")
        .first()
    )

    if version is None:
        version = (
            MaterialVersion.objects.filter(material=material)
            .exclude(status=MaterialVersion.StatusChoices.ARCHIVED)
            .order_by("-version_number", "-created_at")
            .first()
        )

    if version is None:
        Material.objects.filter(id=material.id).update(current_version=None)

        return {
            "material_id": material.id,
            "changed": False,
            "current_version_id": None,
        }

    set_current_material_version(version=version)

    return {
        "material_id": material.id,
        "changed": True,
        "current_version_id": version.id,
    }


@transaction.atomic
def ensure_current_versions_for_materials(
    *,
    material_ids: Iterable[int] | None = None,
) -> dict[str, int]:
    """
    Гарантирует текущие версии для набора материалов.
    """

    queryset = Material.objects.all()

    if material_ids is not None:
        queryset = queryset.filter(id__in=material_ids)

    checked_count = 0
    changed_count = 0

    for material in queryset.iterator():
        result = ensure_current_version_for_material(
            material_id=material.id,
        )

        checked_count += 1

        if result["changed"]:
            changed_count += 1

    return {
        "checked": checked_count,
        "changed": changed_count,
    }


@transaction.atomic
def refresh_material_version_file_metadata(
    *,
    version_id: int,
    calculate_checksum: bool = False,
) -> MaterialVersion:
    """
    Обновляет технические метаданные файла версии материала.
    """

    version = MaterialVersion.objects.select_related("material").get(
        id=version_id,
    )

    if not version.file:
        return version

    if not version.original_filename:
        version.original_filename = version.file.name

    file_size = getattr(version.file, "size", None)

    if file_size is not None:
        version.file_size_bytes = file_size

    guessed_mime_type, _ = mimetypes.guess_type(version.file.name)

    if guessed_mime_type:
        version.mime_type = guessed_mime_type

    if calculate_checksum:
        version.checksum = _calculate_file_checksum(version.file)

    version.full_clean()
    version.save(
        update_fields=[
            "original_filename",
            "mime_type",
            "file_size_bytes",
            "checksum",
            "updated_at",
        ],
    )

    return version


@transaction.atomic
def refresh_material_versions_file_metadata(
    *,
    version_ids: Iterable[int] | None = None,
    calculate_checksum: bool = False,
) -> dict[str, int]:
    """
    Обновляет технические метаданные файлов у набора версий.
    """

    queryset = MaterialVersion.objects.exclude(file="")

    if version_ids is not None:
        queryset = queryset.filter(id__in=version_ids)

    updated_count = 0
    skipped_count = 0

    for version in queryset.iterator():
        if not version.file:
            skipped_count += 1
            continue

        refresh_material_version_file_metadata(
            version_id=version.id,
            calculate_checksum=calculate_checksum,
        )
        updated_count += 1

    return {
        "updated": updated_count,
        "skipped": skipped_count,
    }


def _calculate_file_checksum(file) -> str:
    """
    Считает SHA-256 для файла версии материала.
    """

    sha256 = hashlib.sha256()

    current_position = None

    try:
        current_position = file.tell()
    except (AttributeError, OSError):
        current_position = None

    try:
        file.seek(0)
    except (AttributeError, OSError):
        pass

    for chunk in file.chunks():
        sha256.update(chunk)

    if current_position is not None:
        try:
            file.seek(current_position)
        except (AttributeError, OSError):
            pass

    return sha256.hexdigest()
