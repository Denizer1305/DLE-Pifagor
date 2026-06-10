from __future__ import annotations

from typing import Any

from apps.education.models import TeacherGroupSubject
from apps.education.selectors import get_teacher_group_subject_by_id
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import Sum
from django.utils.translation import gettext_lazy as _

TEACHER_GROUP_SUBJECT_MUTABLE_FIELDS = {
    "teacher",
    "teacher_id",
    "group_subject",
    "group_subject_id",
    "role",
    "is_primary",
    "is_active",
    "planned_hours",
    "starts_at",
    "ends_at",
    "notes",
}


@transaction.atomic
def create_teacher_group_subject(
    *,
    data: dict[str, Any],
) -> TeacherGroupSubject:
    """
    Создаёт назначение преподавателя на предмет группы.
    """

    assignment = TeacherGroupSubject()

    _apply_teacher_group_subject_data(
        assignment=assignment,
        data=data,
    )

    _normalize_teacher_group_subject(assignment=assignment)
    _validate_total_teacher_hours(assignment=assignment)

    if assignment.is_primary:
        _unset_other_primary_assignments(
            group_subject_id=assignment.group_subject_id,
        )

    assignment.full_clean()
    assignment.save()

    return assignment


@transaction.atomic
def update_teacher_group_subject(
    *,
    assignment: TeacherGroupSubject,
    data: dict[str, Any],
) -> TeacherGroupSubject:
    """
    Обновляет назначение преподавателя на предмет группы.
    """

    _apply_teacher_group_subject_data(
        assignment=assignment,
        data=data,
    )

    _normalize_teacher_group_subject(assignment=assignment)
    _validate_total_teacher_hours(assignment=assignment)

    if assignment.is_primary:
        _unset_other_primary_assignments(
            group_subject_id=assignment.group_subject_id,
            exclude_id=assignment.id,
        )

    assignment.full_clean()
    assignment.save()

    return assignment


@transaction.atomic
def update_teacher_group_subject_by_id(
    *,
    assignment_id: int,
    data: dict[str, Any],
) -> TeacherGroupSubject:
    """
    Обновляет назначение преподавателя по идентификатору.
    """

    assignment = get_teacher_group_subject_by_id(assignment_id)

    return update_teacher_group_subject(
        assignment=assignment,
        data=data,
    )


@transaction.atomic
def set_primary_teacher_group_subject(
    *,
    assignment: TeacherGroupSubject,
) -> TeacherGroupSubject:
    """
    Делает преподавателя основным по предмету группы.
    """

    _unset_other_primary_assignments(
        group_subject_id=assignment.group_subject_id,
        exclude_id=assignment.id,
    )

    assignment.is_primary = True
    assignment.role = TeacherGroupSubject.RoleChoices.PRIMARY
    assignment.is_active = True
    assignment.full_clean()
    assignment.save(
        update_fields=[
            "is_primary",
            "role",
            "is_active",
            "updated_at",
        ],
    )

    return assignment


@transaction.atomic
def set_primary_teacher_group_subject_by_id(
    *,
    assignment_id: int,
) -> TeacherGroupSubject:
    """
    Делает преподавателя основным по идентификатору назначения.
    """

    assignment = get_teacher_group_subject_by_id(assignment_id)

    return set_primary_teacher_group_subject(assignment=assignment)


@transaction.atomic
def deactivate_teacher_group_subject(
    *,
    assignment: TeacherGroupSubject,
) -> TeacherGroupSubject:
    """
    Деактивирует назначение преподавателя.
    """

    assignment.is_active = False

    if assignment.is_primary:
        assignment.is_primary = False

    assignment.full_clean()
    assignment.save(
        update_fields=[
            "is_active",
            "is_primary",
            "updated_at",
        ],
    )

    return assignment


@transaction.atomic
def deactivate_teacher_group_subject_by_id(
    *,
    assignment_id: int,
) -> TeacherGroupSubject:
    """
    Деактивирует назначение преподавателя по идентификатору.
    """

    assignment = get_teacher_group_subject_by_id(assignment_id)

    return deactivate_teacher_group_subject(assignment=assignment)


@transaction.atomic
def restore_teacher_group_subject(
    *,
    assignment: TeacherGroupSubject,
) -> TeacherGroupSubject:
    """
    Восстанавливает назначение преподавателя.
    """

    assignment.is_active = True
    assignment.full_clean()
    assignment.save(
        update_fields=[
            "is_active",
            "updated_at",
        ],
    )

    return assignment


@transaction.atomic
def restore_teacher_group_subject_by_id(
    *,
    assignment_id: int,
) -> TeacherGroupSubject:
    """
    Восстанавливает назначение преподавателя по идентификатору.
    """

    assignment = get_teacher_group_subject_by_id(assignment_id)

    return restore_teacher_group_subject(assignment=assignment)


def _apply_teacher_group_subject_data(
    *,
    assignment: TeacherGroupSubject,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к назначению преподавателя.
    """

    for field_name in TEACHER_GROUP_SUBJECT_MUTABLE_FIELDS:
        if field_name in data:
            setattr(assignment, field_name, data[field_name])


def _normalize_teacher_group_subject(
    *,
    assignment: TeacherGroupSubject,
) -> None:
    """
    Нормализует назначение перед валидацией.
    """

    if assignment.is_primary:
        assignment.role = TeacherGroupSubject.RoleChoices.PRIMARY

    if assignment.role == TeacherGroupSubject.RoleChoices.PRIMARY:
        assignment.is_primary = True


def _validate_total_teacher_hours(
    *,
    assignment: TeacherGroupSubject,
) -> None:
    """
    Проверяет, что суммарная нагрузка преподавателей не превышает часы предмета группы.
    """

    if not assignment.group_subject_id:
        return

    existing_hours = (
        TeacherGroupSubject.objects.filter(
            group_subject_id=assignment.group_subject_id,
            is_active=True,
        )
        .exclude(id=assignment.id)
        .aggregate(total=Sum("planned_hours"))["total"]
        or 0
    )

    total_hours = existing_hours + assignment.planned_hours

    if total_hours > assignment.group_subject.planned_hours:
        raise ValidationError(
            {
                "planned_hours": _(
                    "Суммарные часы преподавателей не могут превышать часы предмета группы."
                )
            }
        )


def _unset_other_primary_assignments(
    *,
    group_subject_id: int,
    exclude_id: int | None = None,
) -> None:
    """
    Снимает флаг основного преподавателя с других назначений предмета группы.
    """

    queryset = TeacherGroupSubject.objects.filter(
        group_subject_id=group_subject_id,
        is_primary=True,
    )

    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)

    queryset.update(is_primary=False)
