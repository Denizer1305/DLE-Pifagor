from __future__ import annotations

from apps.materials.models import MaterialVersion
from django.db.models import Q, QuerySet


def material_version_base_queryset() -> QuerySet[MaterialVersion]:
    """
    Возвращает базовый queryset версий материалов.
    """

    return MaterialVersion.objects.select_related(
        "material",
        "created_by",
    )


def material_version_list_queryset(
    *,
    search: str | None = None,
    material_id: int | None = None,
    status: str | None = None,
    created_by_id: int | None = None,
    is_current: bool | None = None,
) -> QuerySet[MaterialVersion]:
    """
    Возвращает список версий материалов.
    """

    queryset = material_version_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(material__title__icontains=search)
            | Q(material__slug__icontains=search)
            | Q(original_filename__icontains=search)
            | Q(mime_type__icontains=search)
            | Q(checksum__icontains=search)
            | Q(change_log__icontains=search)
            | Q(external_url__icontains=search)
            | Q(created_by__email__icontains=search)
            | Q(created_by__first_name__icontains=search)
            | Q(created_by__last_name__icontains=search)
        )

    if material_id:
        queryset = queryset.filter(material_id=material_id)

    if status:
        queryset = queryset.filter(status=status)

    if created_by_id:
        queryset = queryset.filter(created_by_id=created_by_id)

    if is_current is not None:
        queryset = queryset.filter(is_current=is_current)

    return queryset.order_by(
        "material_id",
        "-version_number",
        "-created_at",
    )


def material_version_detail_queryset() -> QuerySet[MaterialVersion]:
    """
    Возвращает queryset версии материала с деталями.
    """

    return material_version_base_queryset()


def get_material_version_by_id(
    version_id: int,
) -> MaterialVersion:
    """
    Возвращает версию материала по идентификатору.
    """

    return material_version_detail_queryset().get(id=version_id)


def get_current_material_version(
    material_id: int,
) -> MaterialVersion | None:
    """
    Возвращает текущую версию материала.
    """

    return (
        material_version_detail_queryset()
        .filter(
            material_id=material_id,
            is_current=True,
        )
        .first()
    )


def get_next_material_version_number(
    material_id: int,
) -> int:
    """
    Возвращает следующий номер версии материала.
    """

    last_version = (
        MaterialVersion.objects.filter(material_id=material_id)
        .order_by("-version_number")
        .first()
    )

    if last_version is None:
        return 1

    return last_version.version_number + 1
