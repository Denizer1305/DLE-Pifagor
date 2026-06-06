from __future__ import annotations

from typing import Any

from apps.organizations.models import Organization
from apps.organizations.selectors import (
    actor_can_admin_organization_id,
    get_admin_organizations_queryset_for_actor,
)
from django.db import IntegrityError, transaction
from rest_framework.exceptions import PermissionDenied, ValidationError


ORGANIZATION_EDITABLE_FIELDS = [
    "name",
    "short_name",
    "slug",
    "code",
    "description",
    "city",
    "address",
    "phone",
    "email",
    "website",
    "logo",
    "is_public",
    "is_default_public",
]
"""
Поля организации, которые можно менять через административный сервис.

is_active меняется отдельными действиями deactivate/restore.
Код регистрации преподавателя меняется отдельным сервисом.
"""


def validate_actor_can_manage_organization(
    *,
    actor,
    organization: Organization | None = None,
) -> None:
    """
    Проверяет, может ли пользователь управлять организацией.

    Args:
        actor:
            Пользователь, выполняющий действие.
        organization:
            Организация. Для создания может быть None.

    Raises:
        PermissionDenied: Если доступа нет.
    """

    if organization is None:
        available_queryset = get_admin_organizations_queryset_for_actor(actor=actor)

        if not available_queryset.exists() and not getattr(actor, "is_superuser", False):
            raise PermissionDenied(
                "У пользователя нет прав управлять организациями."
            )

        return

    if not actor_can_admin_organization_id(
        actor=actor,
        organization_id=organization.id,
    ):
        raise PermissionDenied(
            "Организация недоступна для текущего пользователя."
        )


def normalize_organization_data(*, data: dict[str, Any]) -> dict[str, Any]:
    """
    Оставляет только разрешённые поля организации.

    Args:
        data:
            Исходные данные.

    Returns:
        dict: Очищенные данные.
    """

    return {
        field: data[field]
        for field in ORGANIZATION_EDITABLE_FIELDS
        if field in data
    }


def apply_organization_fields(
    *,
    organization: Organization,
    data: dict[str, Any],
) -> list[str]:
    """
    Применяет изменения к организации.

    Args:
        organization:
            Организация.
        data:
            Данные для изменения.

    Returns:
        list[str]: Список изменённых полей.
    """

    changed_fields = []

    for field, value in data.items():
        old_value = getattr(organization, field)

        if old_value == value:
            continue

        setattr(organization, field, value)
        changed_fields.append(field)

    return changed_fields


def save_organization(
    *,
    organization: Organization,
    update_fields: list[str] | None = None,
) -> Organization:
    """
    Валидирует и сохраняет организацию.

    Args:
        organization:
            Организация.
        update_fields:
            Поля для точечного сохранения.

    Returns:
        Organization: Сохранённая организация.

    Raises:
        ValidationError: Если данные некорректны.
    """

    try:
        organization.full_clean()

        if update_fields:
            organization.save(update_fields=update_fields)
        else:
            organization.save()

    except IntegrityError as error:
        raise ValidationError(
            {
                "detail": (
                    "Не удалось сохранить организацию. "
                    "Проверьте уникальность названия, slug и кода."
                )
            }
        ) from error

    return organization


@transaction.atomic
def create_organization(
    *,
    actor,
    data: dict[str, Any],
) -> Organization:
    """
    Создаёт образовательную организацию.

    Args:
        actor:
            Пользователь, выполняющий действие.
        data:
            Данные организации.

    Returns:
        Organization: Созданная организация.
    """

    validate_actor_can_manage_organization(actor=actor)

    normalized_data = normalize_organization_data(data=data)

    organization = Organization(**normalized_data)

    return save_organization(organization=organization)


@transaction.atomic
def update_organization(
    *,
    actor,
    organization: Organization,
    data: dict[str, Any],
) -> Organization:
    """
    Обновляет образовательную организацию.

    Args:
        actor:
            Пользователь, выполняющий действие.
        organization:
            Организация.
        data:
            Данные обновления.

    Returns:
        Organization: Обновлённая организация.
    """

    validate_actor_can_manage_organization(
        actor=actor,
        organization=organization,
    )

    normalized_data = normalize_organization_data(data=data)

    changed_fields = apply_organization_fields(
        organization=organization,
        data=normalized_data,
    )

    if not changed_fields:
        return organization

    changed_fields.append("updated_at")

    return save_organization(
        organization=organization,
        update_fields=changed_fields,
    )


@transaction.atomic
def deactivate_organization(
    *,
    actor,
    organization: Organization,
) -> Organization:
    """
    Деактивирует образовательную организацию.

    Args:
        actor:
            Пользователь, выполняющий действие.
        organization:
            Организация.

    Returns:
        Organization: Деактивированная организация.
    """

    validate_actor_can_manage_organization(
        actor=actor,
        organization=organization,
    )

    if not organization.is_active:
        raise ValidationError(
            {
                "is_active": "Организация уже деактивирована.",
            }
        )

    organization.is_active = False

    return save_organization(
        organization=organization,
        update_fields=[
            "is_active",
            "updated_at",
        ],
    )


@transaction.atomic
def restore_organization(
    *,
    actor,
    organization: Organization,
) -> Organization:
    """
    Восстанавливает образовательную организацию.

    Args:
        actor:
            Пользователь, выполняющий действие.
        organization:
            Организация.

    Returns:
        Organization: Восстановленная организация.
    """

    validate_actor_can_manage_organization(
        actor=actor,
        organization=organization,
    )

    if organization.is_active:
        raise ValidationError(
            {
                "is_active": "Организация уже активна.",
            }
        )

    organization.is_active = True

    return save_organization(
        organization=organization,
        update_fields=[
            "is_active",
            "updated_at",
        ],
    )