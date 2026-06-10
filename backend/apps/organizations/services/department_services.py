from __future__ import annotations

from typing import Any

from apps.organizations.models import Department, Organization
from apps.organizations.selectors import (
    actor_can_admin_organization_id,
    actor_can_manage_department,
)
from django.db import IntegrityError, transaction
from rest_framework.exceptions import PermissionDenied, ValidationError

DEPARTMENT_EDITABLE_FIELDS = [
    "organization",
    "name",
    "short_name",
    "code",
    "description",
]
"""
Поля отделения, которые можно менять через административный сервис.

is_active меняется отдельными действиями deactivate/restore.
"""


def validate_actor_can_create_department(
    *,
    actor,
    organization: Organization | None,
) -> None:
    """
    Проверяет, может ли пользователь создать отделение в организации.

    Args:
        actor:
            Пользователь, выполняющий действие.
        organization:
            Организация, в которой создаётся отделение.

    Raises:
        PermissionDenied: Если доступа нет.
        ValidationError: Если организация не передана.
    """

    if organization is None:
        raise ValidationError(
            {
                "organization": "Необходимо указать образовательную организацию.",
            }
        )

    if not actor_can_admin_organization_id(
        actor=actor,
        organization_id=organization.id,
    ):
        raise PermissionDenied(
            "У пользователя нет прав создавать отделения в этой организации."
        )


def validate_actor_can_update_department(
    *,
    actor,
    department: Department,
) -> None:
    """
    Проверяет, может ли пользователь управлять отделением.

    Args:
        actor:
            Пользователь, выполняющий действие.
        department:
            Отделение.

    Raises:
        PermissionDenied: Если доступа нет.
    """

    if not actor_can_manage_department(
        actor=actor,
        department=department,
    ):
        raise PermissionDenied("Отделение недоступно для текущего пользователя.")


def normalize_department_data(*, data: dict[str, Any]) -> dict[str, Any]:
    """
    Оставляет только разрешённые поля отделения.

    Args:
        data:
            Исходные данные.

    Returns:
        dict: Очищенные данные.
    """

    return {field: data[field] for field in DEPARTMENT_EDITABLE_FIELDS if field in data}


def apply_department_fields(
    *,
    department: Department,
    data: dict[str, Any],
) -> list[str]:
    """
    Применяет изменения к отделению.

    Args:
        department:
            Отделение.
        data:
            Данные для изменения.

    Returns:
        list[str]: Список изменённых полей.
    """

    changed_fields = []

    for field, value in data.items():
        old_value = getattr(department, field)

        if old_value == value:
            continue

        setattr(department, field, value)
        changed_fields.append(field)

    return changed_fields


def save_department(
    *,
    department: Department,
    update_fields: list[str] | None = None,
) -> Department:
    """
    Валидирует и сохраняет отделение.

    Args:
        department:
            Отделение.
        update_fields:
            Поля для точечного сохранения.

    Returns:
        Department: Сохранённое отделение.

    Raises:
        ValidationError: Если данные некорректны.
    """

    try:
        department.full_clean()

        if update_fields:
            department.save(update_fields=update_fields)
        else:
            department.save()

    except IntegrityError as error:
        raise ValidationError(
            {
                "detail": (
                    "Не удалось сохранить отделение. "
                    "Проверьте уникальность названия и кода внутри организации."
                )
            }
        ) from error

    return department


@transaction.atomic
def create_department(
    *,
    actor,
    organization: Organization,
    data: dict[str, Any],
) -> Department:
    """
    Создаёт отделение образовательной организации.

    Args:
        actor:
            Пользователь, выполняющий действие.
        organization:
            Организация.
        data:
            Данные отделения.

    Returns:
        Department: Созданное отделение.
    """

    validate_actor_can_create_department(
        actor=actor,
        organization=organization,
    )

    normalized_data = normalize_department_data(data=data)
    normalized_data["organization"] = organization

    department = Department(**normalized_data)

    return save_department(department=department)


@transaction.atomic
def update_department(
    *,
    actor,
    department: Department,
    data: dict[str, Any],
) -> Department:
    """
    Обновляет отделение образовательной организации.

    Args:
        actor:
            Пользователь, выполняющий действие.
        department:
            Отделение.
        data:
            Данные обновления.

    Returns:
        Department: Обновлённое отделение.
    """

    validate_actor_can_update_department(
        actor=actor,
        department=department,
    )

    normalized_data = normalize_department_data(data=data)

    if "organization" in normalized_data:
        new_organization = normalized_data["organization"]

        if not actor_can_admin_organization_id(
            actor=actor,
            organization_id=new_organization.id,
        ):
            raise PermissionDenied(
                "Нельзя перенести отделение в недоступную организацию."
            )

    changed_fields = apply_department_fields(
        department=department,
        data=normalized_data,
    )

    if not changed_fields:
        return department

    changed_fields.append("updated_at")

    return save_department(
        department=department,
        update_fields=changed_fields,
    )


@transaction.atomic
def deactivate_department(
    *,
    actor,
    department: Department,
) -> Department:
    """
    Деактивирует отделение.

    Args:
        actor:
            Пользователь, выполняющий действие.
        department:
            Отделение.

    Returns:
        Department: Деактивированное отделение.
    """

    validate_actor_can_update_department(
        actor=actor,
        department=department,
    )

    if not department.is_active:
        raise ValidationError(
            {
                "is_active": "Отделение уже деактивировано.",
            }
        )

    department.is_active = False

    return save_department(
        department=department,
        update_fields=[
            "is_active",
            "updated_at",
        ],
    )


@transaction.atomic
def restore_department(
    *,
    actor,
    department: Department,
) -> Department:
    """
    Восстанавливает отделение.

    Args:
        actor:
            Пользователь, выполняющий действие.
        department:
            Отделение.

    Returns:
        Department: Восстановленное отделение.
    """

    validate_actor_can_update_department(
        actor=actor,
        department=department,
    )

    if department.is_active:
        raise ValidationError(
            {
                "is_active": "Отделение уже активно.",
            }
        )

    if not department.organization.is_active:
        raise ValidationError(
            {"organization": ("Нельзя восстановить отделение неактивной организации.")}
        )

    department.is_active = True

    return save_department(
        department=department,
        update_fields=[
            "is_active",
            "updated_at",
        ],
    )
