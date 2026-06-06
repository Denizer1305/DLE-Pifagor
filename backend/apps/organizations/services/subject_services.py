from __future__ import annotations

from typing import Any

from apps.organizations.models import Subject
from apps.organizations.selectors import actor_has_organization_admin_access
from django.db import IntegrityError, transaction
from rest_framework.exceptions import PermissionDenied, ValidationError


SUBJECT_EDITABLE_FIELDS = [
    "name",
    "short_name",
    "code",
    "description",
]
"""
Поля предмета, которые можно менять через административный сервис.

is_active меняется отдельными действиями deactivate/restore.
"""


def validate_actor_can_manage_subjects(*, actor) -> None:
    """
    Проверяет право управления справочником предметов.

    Args:
        actor:
            Пользователь, выполняющий действие.

    Raises:
        PermissionDenied: Если доступа нет.
    """

    if not actor_has_organization_admin_access(actor=actor):
        raise PermissionDenied(
            "У пользователя нет прав управлять учебными предметами."
        )


def normalize_subject_data(*, data: dict[str, Any]) -> dict[str, Any]:
    """
    Оставляет только разрешённые поля предмета.

    Args:
        data:
            Исходные данные.

    Returns:
        dict: Очищенные данные.
    """

    return {
        field: data[field]
        for field in SUBJECT_EDITABLE_FIELDS
        if field in data
    }


def apply_subject_fields(
    *,
    subject: Subject,
    data: dict[str, Any],
) -> list[str]:
    """
    Применяет изменения к предмету.

    Args:
        subject:
            Учебный предмет.
        data:
            Данные для изменения.

    Returns:
        list[str]: Список изменённых полей.
    """

    changed_fields = []

    for field, value in data.items():
        old_value = getattr(subject, field)

        if old_value == value:
            continue

        setattr(subject, field, value)
        changed_fields.append(field)

    return changed_fields


def save_subject(
    *,
    subject: Subject,
    update_fields: list[str] | None = None,
) -> Subject:
    """
    Валидирует и сохраняет предмет.

    Args:
        subject:
            Учебный предмет.
        update_fields:
            Поля для точечного сохранения.

    Returns:
        Subject: Сохранённый предмет.

    Raises:
        ValidationError: Если данные некорректны.
    """

    try:
        subject.full_clean()

        if update_fields:
            subject.save(update_fields=update_fields)
        else:
            subject.save()

    except IntegrityError as error:
        raise ValidationError(
            {
                "detail": (
                    "Не удалось сохранить предмет. "
                    "Проверьте уникальность названия и кода."
                )
            }
        ) from error

    return subject


@transaction.atomic
def create_subject(
    *,
    actor,
    data: dict[str, Any],
) -> Subject:
    """
    Создаёт учебный предмет.

    Args:
        actor:
            Пользователь, выполняющий действие.
        data:
            Данные предмета.

    Returns:
        Subject: Созданный предмет.
    """

    validate_actor_can_manage_subjects(actor=actor)

    normalized_data = normalize_subject_data(data=data)

    subject = Subject(**normalized_data)

    return save_subject(subject=subject)


@transaction.atomic
def update_subject(
    *,
    actor,
    subject: Subject,
    data: dict[str, Any],
) -> Subject:
    """
    Обновляет учебный предмет.

    Args:
        actor:
            Пользователь, выполняющий действие.
        subject:
            Учебный предмет.
        data:
            Данные обновления.

    Returns:
        Subject: Обновлённый предмет.
    """

    validate_actor_can_manage_subjects(actor=actor)

    normalized_data = normalize_subject_data(data=data)

    changed_fields = apply_subject_fields(
        subject=subject,
        data=normalized_data,
    )

    if not changed_fields:
        return subject

    changed_fields.append("updated_at")

    return save_subject(
        subject=subject,
        update_fields=changed_fields,
    )


@transaction.atomic
def deactivate_subject(
    *,
    actor,
    subject: Subject,
) -> Subject:
    """
    Деактивирует учебный предмет.

    Args:
        actor:
            Пользователь, выполняющий действие.
        subject:
            Учебный предмет.

    Returns:
        Subject: Деактивированный предмет.
    """

    validate_actor_can_manage_subjects(actor=actor)

    if not subject.is_active:
        raise ValidationError(
            {
                "is_active": "Учебный предмет уже деактивирован.",
            }
        )

    subject.is_active = False

    return save_subject(
        subject=subject,
        update_fields=[
            "is_active",
            "updated_at",
        ],
    )


@transaction.atomic
def restore_subject(
    *,
    actor,
    subject: Subject,
) -> Subject:
    """
    Восстанавливает учебный предмет.

    Args:
        actor:
            Пользователь, выполняющий действие.
        subject:
            Учебный предмет.

    Returns:
        Subject: Восстановленный предмет.
    """

    validate_actor_can_manage_subjects(actor=actor)

    if subject.is_active:
        raise ValidationError(
            {
                "is_active": "Учебный предмет уже активен.",
            }
        )

    subject.is_active = True

    return save_subject(
        subject=subject,
        update_fields=[
            "is_active",
            "updated_at",
        ],
    )