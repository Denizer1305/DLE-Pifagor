from __future__ import annotations

from typing import Any

from apps.organizations.models import Organization, TeacherOrganization
from apps.organizations.selectors import (
    actor_can_admin_organization_id,
    actor_can_manage_teacher_organization,
)
from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.constants.roles import RoleCode
from apps.users.models import UserRole
from django.db import IntegrityError, transaction
from rest_framework.exceptions import PermissionDenied, ValidationError

TEACHER_ORGANIZATION_EDITABLE_FIELDS = [
    "organization",
    "position",
    "employment_type",
    "is_primary",
    "is_active",
    "starts_at",
    "ends_at",
    "notes",
]


def user_has_teacher_role(*, user) -> bool:
    """
    Проверяет, есть ли у пользователя активная роль преподавателя.
    """

    if user is None:
        return False

    return UserRole.objects.filter(
        user=user,
        role__code=RoleCode.TEACHER,
        status=UserRoleStatus.ACTIVE,
    ).exists()


def validate_teacher_can_be_attached(*, teacher) -> None:
    """
    Проверяет, можно ли привязать пользователя к организации как преподавателя.
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
                "teacher": "Нельзя привязать неактивного пользователя.",
            }
        )

    if not user_has_teacher_role(user=teacher):
        raise ValidationError(
            {
                "teacher": "Пользователь не имеет активной роли преподавателя.",
            }
        )


def validate_actor_can_attach_teacher_to_organization(
    *,
    actor,
    organization: Organization | None,
) -> None:
    """
    Проверяет право привязки преподавателя к организации.
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
            "У пользователя нет прав управлять преподавателями этой организации."
        )


def validate_actor_can_update_teacher_organization(
    *,
    actor,
    teacher_organization: TeacherOrganization,
) -> None:
    """
    Проверяет право изменения связи преподавателя с организацией.
    """

    if not actor_can_manage_teacher_organization(
        actor=actor,
        teacher_organization=teacher_organization,
    ):
        raise PermissionDenied(
            "Связь преподавателя с организацией недоступна текущему пользователю."
        )


def normalize_teacher_organization_data(
    *,
    data: dict[str, Any],
) -> dict[str, Any]:
    """
    Оставляет только разрешённые поля связи преподавателя с организацией.
    """

    return {
        field: data[field]
        for field in TEACHER_ORGANIZATION_EDITABLE_FIELDS
        if field in data
    }


def apply_teacher_organization_fields(
    *,
    teacher_organization: TeacherOrganization,
    data: dict[str, Any],
) -> list[str]:
    """
    Применяет изменения к связи преподавателя с организацией.
    """

    changed_fields = []

    for field, value in data.items():
        old_value = getattr(teacher_organization, field)

        if old_value == value:
            continue

        setattr(teacher_organization, field, value)
        changed_fields.append(field)

    return changed_fields


def save_teacher_organization(
    *,
    teacher_organization: TeacherOrganization,
    update_fields: list[str] | None = None,
) -> TeacherOrganization:
    """
    Валидирует и сохраняет связь преподавателя с организацией.
    """

    try:
        teacher_organization.full_clean()

        if update_fields:
            teacher_organization.save(update_fields=update_fields)
        else:
            teacher_organization.save()

    except IntegrityError as error:
        raise ValidationError(
            {
                "detail": (
                    "Не удалось сохранить связь преподавателя с организацией. "
                    "Проверьте, что такая связь ещё не существует."
                )
            }
        ) from error

    return teacher_organization


@transaction.atomic
def attach_teacher_to_organization(
    *,
    actor,
    teacher,
    organization: Organization,
    data: dict[str, Any] | None = None,
) -> TeacherOrganization:
    """
    Привязывает преподавателя к образовательной организации.
    """

    validate_actor_can_attach_teacher_to_organization(
        actor=actor,
        organization=organization,
    )
    validate_teacher_can_be_attached(teacher=teacher)

    normalized_data = normalize_teacher_organization_data(data=data or {})
    normalized_data["organization"] = organization

    teacher_organization = TeacherOrganization(
        teacher=teacher,
        **normalized_data,
    )

    return save_teacher_organization(
        teacher_organization=teacher_organization,
    )


@transaction.atomic
def update_teacher_organization(
    *,
    actor,
    teacher_organization: TeacherOrganization,
    data: dict[str, Any],
) -> TeacherOrganization:
    """
    Обновляет связь преподавателя с организацией.
    """

    validate_actor_can_update_teacher_organization(
        actor=actor,
        teacher_organization=teacher_organization,
    )

    normalized_data = normalize_teacher_organization_data(data=data)

    if "organization" in normalized_data:
        new_organization = normalized_data["organization"]

        if not actor_can_admin_organization_id(
            actor=actor,
            organization_id=new_organization.id,
        ):
            raise PermissionDenied(
                "Нельзя перенести преподавателя в недоступную организацию."
            )

    changed_fields = apply_teacher_organization_fields(
        teacher_organization=teacher_organization,
        data=normalized_data,
    )

    if not changed_fields:
        return teacher_organization

    changed_fields.append("updated_at")

    return save_teacher_organization(
        teacher_organization=teacher_organization,
        update_fields=changed_fields,
    )


@transaction.atomic
def detach_teacher_from_organization(
    *,
    actor,
    teacher_organization: TeacherOrganization,
) -> TeacherOrganization:
    """
    Деактивирует связь преподавателя с организацией.
    """

    validate_actor_can_update_teacher_organization(
        actor=actor,
        teacher_organization=teacher_organization,
    )

    if not teacher_organization.is_active:
        raise ValidationError(
            {
                "is_active": "Связь преподавателя с организацией уже неактивна.",
            }
        )

    teacher_organization.is_active = False
    teacher_organization.is_primary = False

    return save_teacher_organization(
        teacher_organization=teacher_organization,
        update_fields=[
            "is_active",
            "is_primary",
            "updated_at",
        ],
    )


@transaction.atomic
def set_primary_teacher_organization(
    *,
    actor,
    teacher_organization: TeacherOrganization,
) -> TeacherOrganization:
    """
    Делает организацию основной для преподавателя.
    """

    validate_actor_can_update_teacher_organization(
        actor=actor,
        teacher_organization=teacher_organization,
    )

    if not teacher_organization.is_active:
        raise ValidationError(
            {
                "is_active": "Нельзя сделать основной неактивную связь.",
            }
        )

    TeacherOrganization.objects.filter(
        teacher=teacher_organization.teacher,
        is_primary=True,
        is_active=True,
    ).exclude(
        id=teacher_organization.id,
    ).update(
        is_primary=False,
    )

    teacher_organization.is_primary = True

    return save_teacher_organization(
        teacher_organization=teacher_organization,
        update_fields=[
            "is_primary",
            "updated_at",
        ],
    )
