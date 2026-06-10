from __future__ import annotations

from typing import Any

from apps.organizations.constants import StudyGroupStatus
from apps.organizations.models import Department, Organization, StudyGroup
from apps.organizations.selectors import (
    actor_can_admin_organization_id,
    actor_can_manage_study_group,
)
from django.db import IntegrityError, transaction
from rest_framework.exceptions import PermissionDenied, ValidationError

STUDY_GROUP_EDITABLE_FIELDS = [
    "organization",
    "department",
    "name",
    "code",
    "admission_year",
    "graduation_year",
    "course_number",
    "study_form",
    "status",
    "description",
]


def validate_department_belongs_to_organization(
    *,
    organization: Organization,
    department: Department | None,
) -> None:
    """
    Проверяет, что отделение принадлежит организации.
    """

    if department is None:
        return

    if department.organization_id != organization.id:
        raise ValidationError(
            {"department": ("Отделение должно принадлежать выбранной организации.")}
        )


def validate_actor_can_create_study_group(
    *,
    actor,
    organization: Organization | None,
) -> None:
    """
    Проверяет право создания группы в организации.
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
            "У пользователя нет прав создавать группы в этой организации."
        )


def validate_actor_can_update_study_group(
    *,
    actor,
    group: StudyGroup,
) -> None:
    """
    Проверяет право управления учебной группой.
    """

    if not actor_can_manage_study_group(
        actor=actor,
        group=group,
    ):
        raise PermissionDenied("Учебная группа недоступна для текущего пользователя.")


def normalize_study_group_data(*, data: dict[str, Any]) -> dict[str, Any]:
    """
    Оставляет только разрешённые поля группы.
    """

    return {
        field: data[field] for field in STUDY_GROUP_EDITABLE_FIELDS if field in data
    }


def apply_study_group_fields(
    *,
    group: StudyGroup,
    data: dict[str, Any],
) -> list[str]:
    """
    Применяет изменения к группе.
    """

    changed_fields = []

    for field, value in data.items():
        old_value = getattr(group, field)

        if old_value == value:
            continue

        setattr(group, field, value)
        changed_fields.append(field)

    return changed_fields


def save_study_group(
    *,
    group: StudyGroup,
    update_fields: list[str] | None = None,
) -> StudyGroup:
    """
    Валидирует и сохраняет учебную группу.
    """

    try:
        group.full_clean()

        if update_fields:
            group.save(update_fields=update_fields)
        else:
            group.save()

    except IntegrityError as error:
        raise ValidationError(
            {
                "detail": (
                    "Не удалось сохранить группу. "
                    "Проверьте уникальность названия и кода внутри организации."
                )
            }
        ) from error

    return group


@transaction.atomic
def create_study_group(
    *,
    actor,
    organization: Organization,
    data: dict[str, Any],
) -> StudyGroup:
    """
    Создаёт учебную группу.
    """

    validate_actor_can_create_study_group(
        actor=actor,
        organization=organization,
    )

    normalized_data = normalize_study_group_data(data=data)
    normalized_data["organization"] = organization

    department = normalized_data.get("department")
    validate_department_belongs_to_organization(
        organization=organization,
        department=department,
    )

    group = StudyGroup(**normalized_data)

    return save_study_group(group=group)


@transaction.atomic
def update_study_group(
    *,
    actor,
    group: StudyGroup,
    data: dict[str, Any],
) -> StudyGroup:
    """
    Обновляет учебную группу.
    """

    validate_actor_can_update_study_group(
        actor=actor,
        group=group,
    )

    normalized_data = normalize_study_group_data(data=data)

    new_organization = normalized_data.get(
        "organization",
        group.organization,
    )
    new_department = normalized_data.get(
        "department",
        group.department,
    )

    if "organization" in normalized_data:
        if not actor_can_admin_organization_id(
            actor=actor,
            organization_id=new_organization.id,
        ):
            raise PermissionDenied("Нельзя перенести группу в недоступную организацию.")

    validate_department_belongs_to_organization(
        organization=new_organization,
        department=new_department,
    )

    changed_fields = apply_study_group_fields(
        group=group,
        data=normalized_data,
    )

    if not changed_fields:
        return group

    changed_fields.extend(["is_active", "is_archived", "updated_at"])

    return save_study_group(
        group=group,
        update_fields=list(dict.fromkeys(changed_fields)),
    )


@transaction.atomic
def archive_study_group(
    *,
    actor,
    group: StudyGroup,
) -> StudyGroup:
    """
    Архивирует учебную группу.
    """

    validate_actor_can_update_study_group(
        actor=actor,
        group=group,
    )

    if group.status == StudyGroupStatus.ARCHIVED:
        raise ValidationError(
            {
                "status": "Учебная группа уже находится в архиве.",
            }
        )

    group.status = StudyGroupStatus.ARCHIVED

    return save_study_group(
        group=group,
        update_fields=[
            "status",
            "is_active",
            "is_archived",
            "updated_at",
        ],
    )


@transaction.atomic
def restore_study_group(
    *,
    actor,
    group: StudyGroup,
) -> StudyGroup:
    """
    Восстанавливает учебную группу из архива.
    """

    validate_actor_can_update_study_group(
        actor=actor,
        group=group,
    )

    if group.status == StudyGroupStatus.ACTIVE:
        raise ValidationError(
            {
                "status": "Учебная группа уже активна.",
            }
        )

    if not group.organization.is_active:
        raise ValidationError(
            {"organization": ("Нельзя восстановить группу неактивной организации.")}
        )

    group.status = StudyGroupStatus.ACTIVE

    return save_study_group(
        group=group,
        update_fields=[
            "status",
            "is_active",
            "is_archived",
            "updated_at",
        ],
    )
