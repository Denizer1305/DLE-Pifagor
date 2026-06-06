from __future__ import annotations

from typing import Any

from apps.organizations.models import GroupCurator, StudyGroup
from apps.organizations.selectors import actor_can_manage_study_group
from apps.organizations.services.teacher_organization_services import (
    user_has_teacher_role,
)
from django.db import IntegrityError, transaction
from rest_framework.exceptions import PermissionDenied, ValidationError


GROUP_CURATOR_EDITABLE_FIELDS = [
    "is_primary",
    "is_active",
    "starts_at",
    "ends_at",
    "notes",
]


def validate_teacher_can_be_group_curator(
    *,
    teacher,
    group: StudyGroup,
) -> None:
    """
    Проверяет, можно ли назначить пользователя куратором группы.
    """

    if teacher is None:
        raise ValidationError(
            {
                "teacher": "Необходимо указать куратора.",
            }
        )

    if not teacher.is_active:
        raise ValidationError(
            {
                "teacher": "Нельзя назначить неактивного пользователя куратором.",
            }
        )

    if not user_has_teacher_role(user=teacher):
        raise ValidationError(
            {
                "teacher": "Куратором может быть пользователь с ролью преподавателя.",
            }
        )


def validate_actor_can_manage_group_curator(
    *,
    actor,
    group: StudyGroup,
) -> None:
    """
    Проверяет право управления кураторами группы.
    """

    if not actor_can_manage_study_group(
        actor=actor,
        group=group,
    ):
        raise PermissionDenied(
            "У пользователя нет прав управлять кураторами этой группы."
        )


def validate_actor_can_update_group_curator(
    *,
    actor,
    group_curator: GroupCurator,
) -> None:
    """
    Проверяет право изменения связи куратора с группой.
    """

    validate_actor_can_manage_group_curator(
        actor=actor,
        group=group_curator.group,
    )


def normalize_group_curator_data(*, data: dict[str, Any]) -> dict[str, Any]:
    """
    Оставляет только разрешённые поля куратора группы.
    """

    return {
        field: data[field]
        for field in GROUP_CURATOR_EDITABLE_FIELDS
        if field in data
    }


def apply_group_curator_fields(
    *,
    group_curator: GroupCurator,
    data: dict[str, Any],
) -> list[str]:
    """
    Применяет изменения к связи куратора с группой.
    """

    changed_fields = []

    for field, value in data.items():
        old_value = getattr(group_curator, field)

        if old_value == value:
            continue

        setattr(group_curator, field, value)
        changed_fields.append(field)

    return changed_fields


def save_group_curator(
    *,
    group_curator: GroupCurator,
    update_fields: list[str] | None = None,
) -> GroupCurator:
    """
    Валидирует и сохраняет связь куратора с группой.
    """

    try:
        group_curator.full_clean()

        if update_fields:
            group_curator.save(update_fields=update_fields)
        else:
            group_curator.save()

    except IntegrityError as error:
        raise ValidationError(
            {
                "detail": (
                    "Не удалось сохранить куратора группы. "
                    "Проверьте, что такой куратор ещё не назначен."
                )
            }
        ) from error

    return group_curator


@transaction.atomic
def assign_group_curator(
    *,
    actor,
    group: StudyGroup,
    teacher,
    data: dict[str, Any] | None = None,
) -> GroupCurator:
    """
    Назначает куратора учебной группы.
    """

    validate_actor_can_manage_group_curator(
        actor=actor,
        group=group,
    )
    validate_teacher_can_be_group_curator(
        teacher=teacher,
        group=group,
    )

    normalized_data = normalize_group_curator_data(data=data or {})

    group_curator = GroupCurator(
        group=group,
        teacher=teacher,
        **normalized_data,
    )

    return save_group_curator(group_curator=group_curator)


@transaction.atomic
def update_group_curator(
    *,
    actor,
    group_curator: GroupCurator,
    data: dict[str, Any],
) -> GroupCurator:
    """
    Обновляет связь куратора с группой.
    """

    validate_actor_can_update_group_curator(
        actor=actor,
        group_curator=group_curator,
    )

    normalized_data = normalize_group_curator_data(data=data)

    changed_fields = apply_group_curator_fields(
        group_curator=group_curator,
        data=normalized_data,
    )

    if not changed_fields:
        return group_curator

    changed_fields.append("updated_at")

    return save_group_curator(
        group_curator=group_curator,
        update_fields=changed_fields,
    )


@transaction.atomic
def remove_group_curator(
    *,
    actor,
    group_curator: GroupCurator,
) -> GroupCurator:
    """
    Деактивирует куратора группы.
    """

    validate_actor_can_update_group_curator(
        actor=actor,
        group_curator=group_curator,
    )

    if not group_curator.is_active:
        raise ValidationError(
            {
                "is_active": "Куратор группы уже неактивен.",
            }
        )

    group_curator.is_active = False
    group_curator.is_primary = False

    return save_group_curator(
        group_curator=group_curator,
        update_fields=[
            "is_active",
            "is_primary",
            "updated_at",
        ],
    )


@transaction.atomic
def set_primary_group_curator(
    *,
    actor,
    group_curator: GroupCurator,
) -> GroupCurator:
    """
    Делает куратора основным для группы.
    """

    validate_actor_can_update_group_curator(
        actor=actor,
        group_curator=group_curator,
    )

    if not group_curator.is_active:
        raise ValidationError(
            {
                "is_active": "Нельзя сделать основным неактивного куратора.",
            }
        )

    GroupCurator.objects.filter(
        group=group_curator.group,
        is_primary=True,
        is_active=True,
    ).exclude(
        id=group_curator.id,
    ).update(
        is_primary=False,
    )

    group_curator.is_primary = True

    return save_group_curator(
        group_curator=group_curator,
        update_fields=[
            "is_primary",
            "updated_at",
        ],
    )