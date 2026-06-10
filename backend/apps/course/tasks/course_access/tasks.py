from __future__ import annotations

from apps.course.models import CourseAccessRule, CourseEnrollment, CourseGroupAccess
from apps.course.services import (
    archive_course_enrollment,
    archive_course_group_access,
    deactivate_course_access_rule,
)
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def deactivate_expired_course_group_accesses() -> dict[str, int]:
    """
    Архивирует групповые доступы к курсам с истёкшим сроком действия.
    """

    now = timezone.now()

    group_accesses = CourseGroupAccess.objects.filter(
        is_active=True,
        ends_at__isnull=False,
        ends_at__lt=now,
    ).order_by("id")

    archived_count = 0

    for group_access in group_accesses:
        archive_course_group_access(group_access=group_access)
        archived_count += 1

    return {
        "archived": archived_count,
    }


@transaction.atomic
def deactivate_expired_course_access_rules() -> dict[str, int]:
    """
    Деактивирует правила доступа к курсам с истёкшим сроком действия.
    """

    now = timezone.now()

    access_rules = CourseAccessRule.objects.filter(
        is_active=True,
        ends_at__isnull=False,
        ends_at__lt=now,
    ).order_by("id")

    deactivated_count = 0

    for access_rule in access_rules:
        deactivate_course_access_rule(access_rule=access_rule)
        deactivated_count += 1

    return {
        "deactivated": deactivated_count,
    }


@transaction.atomic
def archive_cancelled_course_enrollments() -> dict[str, int]:
    """
    Архивирует отменённые записи на курс.
    """

    enrollments = CourseEnrollment.objects.filter(
        status=CourseEnrollment.StatusChoices.CANCELLED,
    ).order_by("id")

    archived_count = 0

    for enrollment in enrollments:
        archive_course_enrollment(enrollment=enrollment)
        archived_count += 1

    return {
        "archived": archived_count,
    }


def collect_course_access_stats() -> dict[str, int]:
    """
    Собирает статистику доступов к курсам.
    """

    return {
        "group_accesses_total": CourseGroupAccess.objects.count(),
        "group_accesses_active": CourseGroupAccess.objects.filter(
            is_active=True,
        ).count(),
        "access_rules_total": CourseAccessRule.objects.count(),
        "access_rules_active": CourseAccessRule.objects.filter(
            is_active=True,
        ).count(),
        "enrollments_total": CourseEnrollment.objects.count(),
        "enrollments_active": CourseEnrollment.objects.exclude(
            status__in=[
                CourseEnrollment.StatusChoices.CANCELLED,
                CourseEnrollment.StatusChoices.ARCHIVED,
            ],
        ).count(),
        "enrollments_completed": CourseEnrollment.objects.filter(
            status=CourseEnrollment.StatusChoices.COMPLETED,
        ).count(),
    }
