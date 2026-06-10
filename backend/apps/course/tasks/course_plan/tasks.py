from __future__ import annotations

from datetime import timedelta

from apps.course.models import CoursePlan, CoursePlanImport
from apps.course.services import archive_course_plan, mark_course_plan_import_failed
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def archive_inactive_course_plans() -> dict[str, int]:
    """
    Архивирует неактивные КТП, которые ещё не переведены в архив.
    """

    plans = (
        CoursePlan.objects.filter(is_active=False)
        .exclude(status=CoursePlan.StatusChoices.ARCHIVED)
        .order_by("id")
    )

    archived_count = 0

    for plan in plans:
        archive_course_plan(plan=plan)
        archived_count += 1

    return {
        "archived": archived_count,
    }


@transaction.atomic
def fail_stale_course_plan_imports(
    *,
    older_than_minutes: int = 60,
) -> dict[str, int]:
    """
    Помечает зависшие импорты КТП как ошибочные.
    """

    cutoff_datetime = timezone.now() - timedelta(minutes=older_than_minutes)

    imports = CoursePlanImport.objects.filter(
        status=CoursePlanImport.StatusChoices.UPLOADED,
        imported_at__lt=cutoff_datetime,
    ).order_by("id")

    failed_count = 0

    for plan_import in imports:
        mark_course_plan_import_failed(
            plan_import=plan_import,
            errors=[
                {
                    "code": "stale_import",
                    "message": "Импорт не был обработан за допустимое время.",
                }
            ],
        )
        failed_count += 1

    return {
        "failed": failed_count,
    }


def collect_course_plan_stats() -> dict[str, int]:
    """
    Собирает статистику КТП.
    """

    return {
        "plans_total": CoursePlan.objects.count(),
        "plans_active": CoursePlan.objects.filter(is_active=True).count(),
        "plans_draft": CoursePlan.objects.filter(
            status=CoursePlan.StatusChoices.DRAFT,
        ).count(),
        "plans_reviewed": CoursePlan.objects.filter(
            status=CoursePlan.StatusChoices.REVIEWED,
        ).count(),
        "plans_approved": CoursePlan.objects.filter(
            status=CoursePlan.StatusChoices.APPROVED,
        ).count(),
        "plans_archived": CoursePlan.objects.filter(
            status=CoursePlan.StatusChoices.ARCHIVED,
        ).count(),
        "imports_total": CoursePlanImport.objects.count(),
        "imports_failed": CoursePlanImport.objects.filter(
            status=CoursePlanImport.StatusChoices.FAILED,
        ).count(),
        "imports_applied": CoursePlanImport.objects.filter(
            status=CoursePlanImport.StatusChoices.APPLIED,
        ).count(),
    }
