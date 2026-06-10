from __future__ import annotations

from typing import Any

from apps.education.models import Curriculum
from apps.education.selectors import get_curriculum_by_id
from django.db import transaction

CURRICULUM_MUTABLE_FIELDS = {
    "organization",
    "organization_id",
    "department",
    "department_id",
    "academic_year",
    "academic_year_id",
    "code",
    "name",
    "description",
    "total_hours",
    "status",
    "is_active",
}


@transaction.atomic
def create_curriculum(*, data: dict[str, Any]) -> Curriculum:
    """
    Создаёт учебный план.
    """

    curriculum = Curriculum()

    _apply_curriculum_data(
        curriculum=curriculum,
        data=data,
    )

    curriculum.full_clean()
    curriculum.save()

    return curriculum


@transaction.atomic
def update_curriculum(
    *,
    curriculum: Curriculum,
    data: dict[str, Any],
) -> Curriculum:
    """
    Обновляет учебный план.
    """

    _apply_curriculum_data(
        curriculum=curriculum,
        data=data,
    )

    curriculum.full_clean()
    curriculum.save()

    return curriculum


@transaction.atomic
def update_curriculum_by_id(
    *,
    curriculum_id: int,
    data: dict[str, Any],
) -> Curriculum:
    """
    Обновляет учебный план по идентификатору.
    """

    curriculum = get_curriculum_by_id(curriculum_id)

    return update_curriculum(
        curriculum=curriculum,
        data=data,
    )


@transaction.atomic
def activate_curriculum(
    *,
    curriculum: Curriculum,
) -> Curriculum:
    """
    Переводит учебный план в активный статус.
    """

    curriculum.status = Curriculum.StatusChoices.ACTIVE
    curriculum.is_active = True
    curriculum.full_clean()
    curriculum.save(
        update_fields=[
            "status",
            "is_active",
            "updated_at",
        ],
    )

    return curriculum


@transaction.atomic
def activate_curriculum_by_id(
    *,
    curriculum_id: int,
) -> Curriculum:
    """
    Активирует учебный план по идентификатору.
    """

    curriculum = get_curriculum_by_id(curriculum_id)

    return activate_curriculum(curriculum=curriculum)


@transaction.atomic
def archive_curriculum(
    *,
    curriculum: Curriculum,
) -> Curriculum:
    """
    Архивирует учебный план.
    """

    curriculum.status = Curriculum.StatusChoices.ARCHIVED
    curriculum.is_active = False
    curriculum.full_clean()
    curriculum.save(
        update_fields=[
            "status",
            "is_active",
            "updated_at",
        ],
    )

    return curriculum


@transaction.atomic
def archive_curriculum_by_id(
    *,
    curriculum_id: int,
) -> Curriculum:
    """
    Архивирует учебный план по идентификатору.
    """

    curriculum = get_curriculum_by_id(curriculum_id)

    return archive_curriculum(curriculum=curriculum)


@transaction.atomic
def restore_curriculum(
    *,
    curriculum: Curriculum,
) -> Curriculum:
    """
    Восстанавливает учебный план в черновик.
    """

    curriculum.status = Curriculum.StatusChoices.DRAFT
    curriculum.is_active = True
    curriculum.full_clean()
    curriculum.save(
        update_fields=[
            "status",
            "is_active",
            "updated_at",
        ],
    )

    return curriculum


@transaction.atomic
def restore_curriculum_by_id(
    *,
    curriculum_id: int,
) -> Curriculum:
    """
    Восстанавливает учебный план по идентификатору.
    """

    curriculum = get_curriculum_by_id(curriculum_id)

    return restore_curriculum(curriculum=curriculum)


def _apply_curriculum_data(
    *,
    curriculum: Curriculum,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к учебному плану.
    """

    for field_name in CURRICULUM_MUTABLE_FIELDS:
        if field_name in data:
            setattr(curriculum, field_name, data[field_name])
