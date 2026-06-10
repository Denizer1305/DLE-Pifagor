from __future__ import annotations

from datetime import timedelta
from typing import Iterable

from apps.materials.models import Material, MaterialUsageLog
from apps.materials.services import (
    archive_material,
    log_material_usage,
    publish_material,
)
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def bulk_publish_materials(
    *,
    material_ids: Iterable[int],
    user=None,
) -> dict[str, int]:
    """
    Публикует набор учебных материалов.
    """

    published_count = 0
    skipped_count = 0

    materials = Material.objects.filter(id__in=material_ids)

    for material in materials:
        if material.status == Material.StatusChoices.PUBLISHED:
            skipped_count += 1
            continue

        publish_material(material=material)

        log_material_usage(
            material=material,
            action=MaterialUsageLog.ActionChoices.PUBLISH,
            context=MaterialUsageLog.ContextChoices.ADMIN,
            user=user,
            metadata={
                "source": "bulk_publish_materials",
            },
        )

        published_count += 1

    return {
        "published": published_count,
        "skipped": skipped_count,
    }


@transaction.atomic
def bulk_archive_materials(
    *,
    material_ids: Iterable[int],
    user=None,
) -> dict[str, int]:
    """
    Архивирует набор учебных материалов.
    """

    archived_count = 0
    skipped_count = 0

    materials = Material.objects.filter(id__in=material_ids)

    for material in materials:
        if material.status == Material.StatusChoices.ARCHIVED:
            skipped_count += 1
            continue

        archive_material(material=material)

        log_material_usage(
            material=material,
            action=MaterialUsageLog.ActionChoices.ARCHIVE,
            context=MaterialUsageLog.ContextChoices.ADMIN,
            user=user,
            metadata={
                "source": "bulk_archive_materials",
            },
        )

        archived_count += 1

    return {
        "archived": archived_count,
        "skipped": skipped_count,
    }


@transaction.atomic
def archive_materials_without_versions(
    *,
    user=None,
) -> dict[str, int]:
    """
    Архивирует активные материалы без версий.

    Задача полезна для обслуживания библиотеки: материал без версии
    невозможно полноценно открыть как файл, ссылку или текст.
    """

    archived_count = 0

    materials = (
        Material.objects.active()
        .filter(current_version__isnull=True)
        .exclude(status=Material.StatusChoices.ARCHIVED)
    )

    for material in materials:
        if material.versions.exists():
            continue

        archive_material(material=material)

        log_material_usage(
            material=material,
            action=MaterialUsageLog.ActionChoices.ARCHIVE,
            context=MaterialUsageLog.ContextChoices.ADMIN,
            user=user,
            metadata={
                "source": "archive_materials_without_versions",
                "reason": "material_has_no_versions",
            },
        )

        archived_count += 1

    return {
        "archived": archived_count,
    }


@transaction.atomic
def cleanup_old_material_usage_logs(
    *,
    older_than_days: int = 365,
) -> dict[str, int]:
    """
    Удаляет старые события журнала использования материалов.
    """

    cutoff_datetime = timezone.now() - timedelta(days=older_than_days)

    queryset = MaterialUsageLog.objects.filter(
        created_at__lt=cutoff_datetime,
    )

    deleted_count = queryset.count()
    queryset.delete()

    return {
        "deleted": deleted_count,
    }


def collect_materials_library_stats() -> dict[str, int]:
    """
    Собирает базовую статистику библиотеки материалов.
    """

    return {
        "total": Material.objects.count(),
        "active": Material.objects.active().count(),
        "draft": Material.objects.draft().count(),
        "published": Material.objects.published().count(),
        "archived": Material.objects.archived().count(),
        "without_current_version": Material.objects.filter(
            current_version__isnull=True,
        ).count(),
    }
