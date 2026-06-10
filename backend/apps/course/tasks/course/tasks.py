from __future__ import annotations

from collections.abc import Iterable
from datetime import timedelta

from apps.course.models import Course
from apps.course.services import archive_course, publish_course, restore_course
from django.db import transaction
from django.db.models import Count
from django.utils import timezone


@transaction.atomic
def bulk_publish_courses(
    *,
    course_ids: Iterable[int],
) -> dict[str, int]:
    """
    Публикует набор курсов.
    """

    published_count = 0
    skipped_count = 0

    courses = Course.objects.filter(id__in=course_ids)

    for course in courses:
        if course.status == Course.StatusChoices.PUBLISHED:
            skipped_count += 1
            continue

        publish_course(course=course)
        published_count += 1

    return {
        "published": published_count,
        "skipped": skipped_count,
    }


@transaction.atomic
def bulk_archive_courses(
    *,
    course_ids: Iterable[int],
) -> dict[str, int]:
    """
    Архивирует набор курсов.
    """

    archived_count = 0
    skipped_count = 0

    courses = Course.objects.filter(id__in=course_ids)

    for course in courses:
        if course.status == Course.StatusChoices.ARCHIVED:
            skipped_count += 1
            continue

        archive_course(course=course)
        archived_count += 1

    return {
        "archived": archived_count,
        "skipped": skipped_count,
    }


@transaction.atomic
def bulk_restore_courses(
    *,
    course_ids: Iterable[int],
) -> dict[str, int]:
    """
    Восстанавливает набор курсов в черновики.
    """

    restored_count = 0
    skipped_count = 0

    courses = Course.objects.filter(id__in=course_ids)

    for course in courses:
        if course.status != Course.StatusChoices.ARCHIVED:
            skipped_count += 1
            continue

        restore_course(course=course)
        restored_count += 1

    return {
        "restored": restored_count,
        "skipped": skipped_count,
    }


@transaction.atomic
def archive_expired_courses(
    *,
    older_than_days: int = 30,
) -> dict[str, int]:
    """
    Архивирует активные курсы, срок окончания которых давно прошёл.
    """

    cutoff_datetime = timezone.now() - timedelta(days=older_than_days)

    courses = (
        Course.objects.filter(
            is_active=True,
            ends_at__lt=cutoff_datetime,
        )
        .exclude(status=Course.StatusChoices.ARCHIVED)
        .order_by("id")
    )

    archived_count = 0

    for course in courses:
        archive_course(course=course)
        archived_count += 1

    return {
        "archived": archived_count,
    }


def collect_course_catalog_stats() -> dict[str, int]:
    """
    Собирает базовую статистику каталога курсов.
    """

    return {
        "total": Course.objects.count(),
        "active": Course.objects.filter(is_active=True).count(),
        "draft": Course.objects.filter(
            status=Course.StatusChoices.DRAFT,
        ).count(),
        "published": Course.objects.filter(
            status=Course.StatusChoices.PUBLISHED,
        ).count(),
        "archived": Course.objects.filter(
            status=Course.StatusChoices.ARCHIVED,
        ).count(),
        "templates": Course.objects.filter(is_template=True).count(),
    }


def collect_course_distribution_by_status() -> dict[str, int]:
    """
    Собирает распределение курсов по статусам.
    """

    rows = (
        Course.objects.values("status").annotate(total=Count("id")).order_by("status")
    )

    return {row["status"]: row["total"] for row in rows}
