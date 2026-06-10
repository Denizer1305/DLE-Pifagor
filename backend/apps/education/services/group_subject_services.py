from __future__ import annotations

from typing import Any

from apps.education.models import GroupSubject
from apps.education.selectors import get_group_subject_by_id
from django.db import transaction

GROUP_SUBJECT_MUTABLE_FIELDS = {
    "group",
    "group_id",
    "subject",
    "subject_id",
    "academic_year",
    "academic_year_id",
    "period",
    "period_id",
    "curriculum_item",
    "curriculum_item_id",
    "planned_hours",
    "contact_hours",
    "independent_hours",
    "assessment_type",
    "is_required",
    "is_active",
    "notes",
}


@transaction.atomic
def create_group_subject(*, data: dict[str, Any]) -> GroupSubject:
    """
    Создаёт предмет учебной группы.
    """

    group_subject = GroupSubject()

    _apply_group_subject_data(
        group_subject=group_subject,
        data=data,
    )

    _fill_group_subject_from_curriculum_item(group_subject=group_subject)

    group_subject.full_clean()
    group_subject.save()

    return group_subject


@transaction.atomic
def update_group_subject(
    *,
    group_subject: GroupSubject,
    data: dict[str, Any],
) -> GroupSubject:
    """
    Обновляет предмет учебной группы.
    """

    _apply_group_subject_data(
        group_subject=group_subject,
        data=data,
    )

    _fill_group_subject_from_curriculum_item(group_subject=group_subject)

    group_subject.full_clean()
    group_subject.save()

    return group_subject


@transaction.atomic
def update_group_subject_by_id(
    *,
    group_subject_id: int,
    data: dict[str, Any],
) -> GroupSubject:
    """
    Обновляет предмет учебной группы по идентификатору.
    """

    group_subject = get_group_subject_by_id(group_subject_id)

    return update_group_subject(
        group_subject=group_subject,
        data=data,
    )


@transaction.atomic
def deactivate_group_subject(
    *,
    group_subject: GroupSubject,
) -> GroupSubject:
    """
    Деактивирует предмет учебной группы.
    """

    group_subject.is_active = False
    group_subject.full_clean()
    group_subject.save(
        update_fields=[
            "is_active",
            "updated_at",
        ],
    )

    return group_subject


@transaction.atomic
def deactivate_group_subject_by_id(
    *,
    group_subject_id: int,
) -> GroupSubject:
    """
    Деактивирует предмет учебной группы по идентификатору.
    """

    group_subject = get_group_subject_by_id(group_subject_id)

    return deactivate_group_subject(group_subject=group_subject)


@transaction.atomic
def restore_group_subject(
    *,
    group_subject: GroupSubject,
) -> GroupSubject:
    """
    Восстанавливает предмет учебной группы.
    """

    group_subject.is_active = True
    group_subject.full_clean()
    group_subject.save(
        update_fields=[
            "is_active",
            "updated_at",
        ],
    )

    return group_subject


@transaction.atomic
def restore_group_subject_by_id(
    *,
    group_subject_id: int,
) -> GroupSubject:
    """
    Восстанавливает предмет учебной группы по идентификатору.
    """

    group_subject = get_group_subject_by_id(group_subject_id)

    return restore_group_subject(group_subject=group_subject)


def _apply_group_subject_data(
    *,
    group_subject: GroupSubject,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к предмету учебной группы.
    """

    for field_name in GROUP_SUBJECT_MUTABLE_FIELDS:
        if field_name in data:
            setattr(group_subject, field_name, data[field_name])


def _fill_group_subject_from_curriculum_item(
    *,
    group_subject: GroupSubject,
) -> None:
    """
    Заполняет часть данных предмета группы из элемента учебного плана,
    если они не переданы явно.
    """

    if not group_subject.curriculum_item_id:
        return

    curriculum_item = group_subject.curriculum_item

    if not group_subject.subject_id:
        group_subject.subject = curriculum_item.subject

    if not group_subject.period_id:
        group_subject.period = curriculum_item.period

    if not group_subject.academic_year_id:
        group_subject.academic_year = curriculum_item.curriculum.academic_year

    if not group_subject.planned_hours:
        group_subject.planned_hours = curriculum_item.planned_hours

    if not group_subject.contact_hours:
        group_subject.contact_hours = curriculum_item.contact_hours

    if not group_subject.independent_hours:
        group_subject.independent_hours = curriculum_item.independent_hours

    if group_subject.assessment_type == GroupSubject.AssessmentTypeChoices.NONE:
        group_subject.assessment_type = curriculum_item.assessment_type

    group_subject.is_required = curriculum_item.is_required
