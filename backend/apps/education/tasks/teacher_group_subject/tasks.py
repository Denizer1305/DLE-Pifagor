from __future__ import annotations

from datetime import date

from apps.education.models import TeacherGroupSubject
from apps.education.services import deactivate_teacher_group_subject
from django.utils import timezone


def deactivate_expired_teacher_assignments(
    *,
    reference_date: date | None = None,
) -> dict[str, int]:
    """
    Деактивирует назначения преподавателей с истёкшей датой окончания.
    """

    current_date = reference_date or timezone.localdate()

    assignments = TeacherGroupSubject.objects.filter(
        is_active=True,
        ends_at__isnull=False,
        ends_at__lt=current_date,
    )

    updated_count = 0

    for assignment in assignments:
        deactivate_teacher_group_subject(assignment=assignment)
        updated_count += 1

    return {
        "updated": updated_count,
    }


def deactivate_assignments_for_inactive_group_subjects() -> dict[str, int]:
    """
    Деактивирует назначения преподавателей по неактивным предметам групп.
    """

    assignments = TeacherGroupSubject.objects.filter(
        is_active=True,
        group_subject__is_active=False,
    )

    updated_count = 0

    for assignment in assignments:
        deactivate_teacher_group_subject(assignment=assignment)
        updated_count += 1

    return {
        "updated": updated_count,
    }
