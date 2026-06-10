from __future__ import annotations

from apps.materials.models import Material, MaterialVersion
from apps.materials.selectors import get_material_version_by_id
from django.db import transaction


@transaction.atomic
def set_current_material_version(
    *,
    version: MaterialVersion,
) -> MaterialVersion:
    """
    Делает версию текущей для материала.
    """

    _unset_current_material_versions(
        material_id=version.material_id,
        exclude_id=version.id,
    )

    version.is_current = True
    version.status = MaterialVersion.StatusChoices.CURRENT
    version.full_clean()
    version.save(
        update_fields=[
            "status",
            "is_current",
            "updated_at",
        ],
    )

    Material.objects.filter(id=version.material_id).update(
        current_version=version,
    )

    return version


@transaction.atomic
def set_current_material_version_by_id(
    *,
    version_id: int,
) -> MaterialVersion:
    """
    Делает версию материала текущей по идентификатору.
    """

    version = get_material_version_by_id(version_id)

    return set_current_material_version(version=version)


def _unset_current_material_versions(
    *,
    material_id: int,
    exclude_id: int | None = None,
) -> None:
    """
    Снимает флаг текущей версии с остальных версий материала.
    """

    queryset = MaterialVersion.objects.filter(
        material_id=material_id,
        is_current=True,
    )

    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)

    queryset.update(
        is_current=False,
        status=MaterialVersion.StatusChoices.ARCHIVED,
    )
