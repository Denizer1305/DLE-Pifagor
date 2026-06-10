from __future__ import annotations

from datetime import date

from apps.education.models import Curriculum, GroupSubject
from apps.education.services import create_group_subject, deactivate_group_subject
from apps.organizations.models import StudyGroup
from django.db import IntegrityError
from django.utils import timezone


def sync_group_subjects_from_curriculum(
    *,
    curriculum_id: int,
    group_id: int,
) -> dict[str, int]:
    """
    Создаёт предметы группы по активным элементам учебного плана.

    Уже существующие предметы не дублируются.
    """

    curriculum = Curriculum.objects.get(id=curriculum_id)
    group = StudyGroup.objects.get(id=group_id)

    created_count = 0
    skipped_count = 0

    curriculum_items = curriculum.items.filter(is_active=True).select_related(
        "period",
        "subject",
        "curriculum",
        "curriculum__academic_year",
    )

    for item in curriculum_items:
        exists = GroupSubject.objects.filter(
            group=group,
            subject=item.subject,
            academic_year=curriculum.academic_year,
            period=item.period,
        ).exists()

        if exists:
            skipped_count += 1
            continue

        try:
            create_group_subject(
                data={
                    "group": group,
                    "subject": item.subject,
                    "academic_year": curriculum.academic_year,
                    "period": item.period,
                    "curriculum_item": item,
                    "planned_hours": item.planned_hours,
                    "contact_hours": item.contact_hours,
                    "independent_hours": item.independent_hours,
                    "assessment_type": item.assessment_type,
                    "is_required": item.is_required,
                    "is_active": True,
                    "notes": "",
                }
            )
            created_count += 1
        except IntegrityError:
            skipped_count += 1

    return {
        "created": created_count,
        "skipped": skipped_count,
    }


def deactivate_group_subjects_for_finished_periods(
    *,
    reference_date: date | None = None,
) -> dict[str, int]:
    """
    Деактивирует предметы групп, у которых учебный период завершён.
    """

    current_date = reference_date or timezone.localdate()

    group_subjects = GroupSubject.objects.filter(
        is_active=True,
        period__end_date__lt=current_date,
    )

    updated_count = 0

    for group_subject in group_subjects:
        deactivate_group_subject(group_subject=group_subject)
        updated_count += 1

    return {
        "updated": updated_count,
    }


def deactivate_group_subjects_for_inactive_periods() -> dict[str, int]:
    """
    Деактивирует предметы групп, связанные с неактивными периодами.
    """

    group_subjects = GroupSubject.objects.filter(
        is_active=True,
        period__is_active=False,
    )

    updated_count = 0

    for group_subject in group_subjects:
        deactivate_group_subject(group_subject=group_subject)
        updated_count += 1

    return {
        "updated": updated_count,
    }
