from __future__ import annotations

import secrets

from apps.organizations.constants import (
    MAX_TEACHER_REGISTRATION_CODE_LENGTH,
    MIN_TEACHER_REGISTRATION_CODE_LENGTH,
)
from apps.organizations.models import Organization
from apps.organizations.selectors import actor_can_admin_organization_id
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError


def generate_teacher_registration_code() -> str:
    """
    Генерирует код регистрации преподавателя.

    Returns:
        str: Открытое значение кода.
    """

    return secrets.token_urlsafe(12)[:MAX_TEACHER_REGISTRATION_CODE_LENGTH]


def validate_actor_can_manage_teacher_registration_code(
    *,
    actor,
    organization: Organization,
) -> None:
    """
    Проверяет право управления кодом регистрации преподавателя.
    """

    if not actor_can_admin_organization_id(
        actor=actor,
        organization_id=organization.id,
    ):
        raise PermissionDenied(
            "У пользователя нет прав управлять кодом регистрации этой организации."
        )


@transaction.atomic
def set_teacher_registration_code(
    *,
    actor,
    organization: Organization,
    raw_code: str = "",
    expires_at=None,
) -> tuple[Organization, str]:
    """
    Устанавливает код регистрации преподавателя.

    Если raw_code не передан, генерирует новый код.
    Открытое значение возвращается только в момент установки.
    """

    validate_actor_can_manage_teacher_registration_code(
        actor=actor,
        organization=organization,
    )

    code = raw_code.strip() if raw_code else generate_teacher_registration_code()

    if len(code) < MIN_TEACHER_REGISTRATION_CODE_LENGTH:
        raise ValidationError(
            {
                "teacher_registration_code": (
                    "Код регистрации преподавателя короче минимальной длины."
                )
            }
        )

    organization.set_teacher_registration_code(
        code,
        expires_at=expires_at,
        save=True,
    )

    return organization, code


@transaction.atomic
def disable_teacher_registration_code(
    *,
    actor,
    organization: Organization,
) -> Organization:
    """
    Отключает код регистрации преподавателя.
    """

    validate_actor_can_manage_teacher_registration_code(
        actor=actor,
        organization=organization,
    )

    if not organization.teacher_registration_code_is_active:
        raise ValidationError(
            {
                "teacher_registration_code_is_active": (
                    "Код регистрации преподавателя уже отключён."
                )
            }
        )

    organization.disable_teacher_registration_code(save=True)

    return organization


@transaction.atomic
def clear_teacher_registration_code(
    *,
    actor,
    organization: Organization,
) -> Organization:
    """
    Полностью очищает код регистрации преподавателя.
    """

    validate_actor_can_manage_teacher_registration_code(
        actor=actor,
        organization=organization,
    )

    organization.clear_teacher_registration_code(save=True)

    return organization


def verify_teacher_registration_code(
    *,
    organization: Organization,
    raw_code: str,
) -> bool:
    """
    Проверяет код регистрации преподавателя.
    """

    if organization is None:
        return False

    return organization.verify_teacher_registration_code(raw_code)