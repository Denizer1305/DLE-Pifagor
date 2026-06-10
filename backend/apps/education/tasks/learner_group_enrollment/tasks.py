from __future__ import annotations

from datetime import date

from apps.education.constants import FINISHED_ENROLLMENT_STATUS_CODES
from apps.education.models import LearnerGroupEnrollment
from django.db import transaction
from django.utils import timezone


@transaction.atomic
def normalize_finished_enrollments_primary_flags() -> dict[str, int]:
    """
    Снимает флаг основного зачисления у завершённых зачислений.

    Нужна как безопасная обслуживающая задача для импортированных
    или вручную изменённых данных.
    """

    enrollments = LearnerGroupEnrollment.objects.filter(
        status__in=FINISHED_ENROLLMENT_STATUS_CODES,
        is_primary=True,
    )

    updated_count = 0

    for enrollment in enrollments:
        enrollment.is_primary = False
        enrollment.full_clean()
        enrollment.save(
            update_fields=[
                "is_primary",
                "updated_at",
            ],
        )
        updated_count += 1

    return {
        "updated": updated_count,
    }


@transaction.atomic
def assign_missing_journal_numbers(
    *,
    group_id: int,
    academic_year_id: int,
    start_number: int = 1,
) -> dict[str, int]:
    """
    Назначает номера в журнале активным зачислениям группы.

    Существующие номера не перезаписываются.
    """

    existing_numbers = set(
        LearnerGroupEnrollment.objects.filter(
            group_id=group_id,
            academic_year_id=academic_year_id,
            journal_number__isnull=False,
        ).values_list("journal_number", flat=True)
    )

    enrollments = LearnerGroupEnrollment.objects.filter(
        group_id=group_id,
        academic_year_id=academic_year_id,
        status=LearnerGroupEnrollment.StatusChoices.ACTIVE,
        journal_number__isnull=True,
    ).order_by(
        "learner__last_name",
        "learner__first_name",
        "learner__email",
        "id",
    )

    next_number = start_number
    updated_count = 0

    for enrollment in enrollments:
        while next_number in existing_numbers:
            next_number += 1

        enrollment.journal_number = next_number
        enrollment.full_clean()
        enrollment.save(
            update_fields=[
                "journal_number",
                "updated_at",
            ],
        )

        existing_numbers.add(next_number)
        next_number += 1
        updated_count += 1

    return {
        "updated": updated_count,
    }


def get_active_enrollments_without_journal_numbers_count(
    *,
    group_id: int | None = None,
    academic_year_id: int | None = None,
) -> dict[str, int]:
    """
    Возвращает количество активных зачислений без номера в журнале.
    """

    queryset = LearnerGroupEnrollment.objects.filter(
        status=LearnerGroupEnrollment.StatusChoices.ACTIVE,
        journal_number__isnull=True,
    )

    if group_id:
        queryset = queryset.filter(group_id=group_id)

    if academic_year_id:
        queryset = queryset.filter(academic_year_id=academic_year_id)

    return {
        "count": queryset.count(),
    }


@transaction.atomic
def archive_finished_enrollments_before_date(
    *,
    reference_date: date | None = None,
) -> dict[str, int]:
    """
    Архивирует завершённые зачисления, завершившиеся до указанной даты.

    Активные зачисления не трогает.
    """

    current_date = reference_date or timezone.localdate()

    enrollments = LearnerGroupEnrollment.objects.filter(
        status__in={
            LearnerGroupEnrollment.StatusChoices.TRANSFERRED,
            LearnerGroupEnrollment.StatusChoices.GRADUATED,
            LearnerGroupEnrollment.StatusChoices.EXPELLED,
        },
        completion_date__lt=current_date,
    )

    updated_count = 0

    for enrollment in enrollments:
        enrollment.status = LearnerGroupEnrollment.StatusChoices.ARCHIVED
        enrollment.is_primary = False
        enrollment.full_clean()
        enrollment.save(
            update_fields=[
                "status",
                "is_primary",
                "updated_at",
            ],
        )
        updated_count += 1

    return {
        "updated": updated_count,
    }
