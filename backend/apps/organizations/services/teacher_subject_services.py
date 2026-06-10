from __future__ import annotations

from typing import Any

from apps.organizations.models import Subject, TeacherSubject
from apps.organizations.selectors import actor_has_organization_admin_access
from apps.organizations.services.teacher_organization_services import (
    user_has_teacher_role,
)
from django.db import IntegrityError, transaction
from rest_framework.exceptions import PermissionDenied, ValidationError

TEACHER_SUBJECT_EDITABLE_FIELDS = [
    "subject",
    "is_primary",
    "is_active",
    "notes",
]
"""
Поля связи преподавателя с предметом.

teacher задаётся только при создании связи.
"""


def validate_actor_can_manage_teacher_subjects(*, actor) -> None:
    """
    Проверяет право управления предметами преподавателей.

    Args:
        actor:
            Пользователь, выполняющий действие.

    Raises:
        PermissionDenied: Если доступа нет.
    """

    if not actor_has_organization_admin_access(actor=actor):
        raise PermissionDenied(
            "У пользователя нет прав управлять предметами преподавателей."
        )


def validate_teacher_can_have_subject(*, teacher) -> None:
    """
    Проверяет, может ли пользователь иметь предмет преподавателя.

    Args:
        teacher:
            Пользователь-преподаватель.

    Raises:
        ValidationError: Если пользователь не подходит.
    """

    if teacher is None:
        raise ValidationError(
            {
                "teacher": "Необходимо указать преподавателя.",
            }
        )

    if not teacher.is_active:
        raise ValidationError(
            {
                "teacher": "Нельзя назначить предмет неактивному пользователю.",
            }
        )

    if not user_has_teacher_role(user=teacher):
        raise ValidationError(
            {
                "teacher": "Пользователь не имеет активной роли преподавателя.",
            }
        )


def validate_subject_can_be_assigned(*, subject: Subject | None) -> None:
    """
    Проверяет, можно ли назначить предмет преподавателю.

    Args:
        subject:
            Учебный предмет.

    Raises:
        ValidationError: Если предмет не подходит.
    """

    if subject is None:
        raise ValidationError(
            {
                "subject": "Необходимо указать учебный предмет.",
            }
        )

    if not subject.is_active:
        raise ValidationError(
            {
                "subject": "Нельзя назначить неактивный учебный предмет.",
            }
        )


def normalize_teacher_subject_data(*, data: dict[str, Any]) -> dict[str, Any]:
    """
    Оставляет только разрешённые поля связи преподавателя с предметом.

    Args:
        data:
            Исходные данные.

    Returns:
        dict: Очищенные данные.
    """

    return {
        field: data[field] for field in TEACHER_SUBJECT_EDITABLE_FIELDS if field in data
    }


def apply_teacher_subject_fields(
    *,
    teacher_subject: TeacherSubject,
    data: dict[str, Any],
) -> list[str]:
    """
    Применяет изменения к связи преподавателя с предметом.

    Args:
        teacher_subject:
            Связь преподавателя с предметом.
        data:
            Данные для изменения.

    Returns:
        list[str]: Список изменённых полей.
    """

    changed_fields = []

    for field, value in data.items():
        old_value = getattr(teacher_subject, field)

        if old_value == value:
            continue

        setattr(teacher_subject, field, value)
        changed_fields.append(field)

    return changed_fields


def save_teacher_subject(
    *,
    teacher_subject: TeacherSubject,
    update_fields: list[str] | None = None,
) -> TeacherSubject:
    """
    Валидирует и сохраняет связь преподавателя с предметом.

    Args:
        teacher_subject:
            Связь преподавателя с предметом.
        update_fields:
            Поля для точечного сохранения.

    Returns:
        TeacherSubject: Сохранённая связь.

    Raises:
        ValidationError: Если данные некорректны.
    """

    try:
        teacher_subject.full_clean()

        if update_fields:
            teacher_subject.save(update_fields=update_fields)
        else:
            teacher_subject.save()

    except IntegrityError as error:
        raise ValidationError(
            {
                "detail": (
                    "Не удалось сохранить предмет преподавателя. "
                    "Проверьте, что такая связь ещё не существует."
                )
            }
        ) from error

    return teacher_subject


@transaction.atomic
def assign_subject_to_teacher(
    *,
    actor,
    teacher,
    subject: Subject,
    data: dict[str, Any] | None = None,
) -> TeacherSubject:
    """
    Назначает предмет преподавателю.

    Args:
        actor:
            Пользователь, выполняющий действие.
        teacher:
            Пользователь-преподаватель.
        subject:
            Учебный предмет.
        data:
            Дополнительные данные связи.

    Returns:
        TeacherSubject: Созданная связь.
    """

    validate_actor_can_manage_teacher_subjects(actor=actor)
    validate_teacher_can_have_subject(teacher=teacher)
    validate_subject_can_be_assigned(subject=subject)

    normalized_data = normalize_teacher_subject_data(data=data or {})
    normalized_data["subject"] = subject

    teacher_subject = TeacherSubject(
        teacher=teacher,
        **normalized_data,
    )

    return save_teacher_subject(teacher_subject=teacher_subject)


@transaction.atomic
def update_teacher_subject(
    *,
    actor,
    teacher_subject: TeacherSubject,
    data: dict[str, Any],
) -> TeacherSubject:
    """
    Обновляет предмет преподавателя.

    Args:
        actor:
            Пользователь, выполняющий действие.
        teacher_subject:
            Связь преподавателя с предметом.
        data:
            Данные обновления.

    Returns:
        TeacherSubject: Обновлённая связь.
    """

    validate_actor_can_manage_teacher_subjects(actor=actor)

    normalized_data = normalize_teacher_subject_data(data=data)

    if "subject" in normalized_data:
        validate_subject_can_be_assigned(
            subject=normalized_data["subject"],
        )

    changed_fields = apply_teacher_subject_fields(
        teacher_subject=teacher_subject,
        data=normalized_data,
    )

    if not changed_fields:
        return teacher_subject

    changed_fields.append("updated_at")

    return save_teacher_subject(
        teacher_subject=teacher_subject,
        update_fields=changed_fields,
    )


@transaction.atomic
def deactivate_teacher_subject(
    *,
    actor,
    teacher_subject: TeacherSubject,
) -> TeacherSubject:
    """
    Деактивирует предмет преподавателя.

    Args:
        actor:
            Пользователь, выполняющий действие.
        teacher_subject:
            Связь преподавателя с предметом.

    Returns:
        TeacherSubject: Деактивированная связь.
    """

    validate_actor_can_manage_teacher_subjects(actor=actor)

    if not teacher_subject.is_active:
        raise ValidationError(
            {
                "is_active": "Предмет преподавателя уже деактивирован.",
            }
        )

    teacher_subject.is_active = False
    teacher_subject.is_primary = False

    return save_teacher_subject(
        teacher_subject=teacher_subject,
        update_fields=[
            "is_active",
            "is_primary",
            "updated_at",
        ],
    )


@transaction.atomic
def restore_teacher_subject(
    *,
    actor,
    teacher_subject: TeacherSubject,
) -> TeacherSubject:
    """
    Восстанавливает предмет преподавателя.

    Args:
        actor:
            Пользователь, выполняющий действие.
        teacher_subject:
            Связь преподавателя с предметом.

    Returns:
        TeacherSubject: Восстановленная связь.
    """

    validate_actor_can_manage_teacher_subjects(actor=actor)

    if teacher_subject.is_active:
        raise ValidationError(
            {
                "is_active": "Предмет преподавателя уже активен.",
            }
        )

    validate_subject_can_be_assigned(subject=teacher_subject.subject)
    validate_teacher_can_have_subject(teacher=teacher_subject.teacher)

    teacher_subject.is_active = True

    return save_teacher_subject(
        teacher_subject=teacher_subject,
        update_fields=[
            "is_active",
            "updated_at",
        ],
    )


@transaction.atomic
def set_primary_teacher_subject(
    *,
    actor,
    teacher_subject: TeacherSubject,
) -> TeacherSubject:
    """
    Делает предмет основным для преподавателя.

    Args:
        actor:
            Пользователь, выполняющий действие.
        teacher_subject:
            Связь преподавателя с предметом.

    Returns:
        TeacherSubject: Основной предмет преподавателя.
    """

    validate_actor_can_manage_teacher_subjects(actor=actor)

    if not teacher_subject.is_active:
        raise ValidationError(
            {
                "is_active": "Нельзя сделать основным неактивный предмет.",
            }
        )

    validate_subject_can_be_assigned(subject=teacher_subject.subject)

    TeacherSubject.objects.filter(
        teacher=teacher_subject.teacher,
        is_primary=True,
        is_active=True,
    ).exclude(
        id=teacher_subject.id,
    ).update(
        is_primary=False,
    )

    teacher_subject.is_primary = True

    return save_teacher_subject(
        teacher_subject=teacher_subject,
        update_fields=[
            "is_primary",
            "updated_at",
        ],
    )
