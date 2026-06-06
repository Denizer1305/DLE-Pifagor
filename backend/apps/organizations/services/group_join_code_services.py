from __future__ import annotations

import secrets

from apps.organizations.constants import (
    MAX_GROUP_JOIN_CODE_LENGTH,
    MIN_GROUP_JOIN_CODE_LENGTH,
)
from apps.organizations.models import StudyGroup
from apps.organizations.selectors import actor_can_manage_study_group
from django.db import transaction
from rest_framework.exceptions import PermissionDenied, ValidationError


def generate_group_join_code() -> str:
    """
    Генерирует код вступления в группу.

    Returns:
        str: Открытое значение кода.
    """

    return secrets.token_urlsafe(10)[:MAX_GROUP_JOIN_CODE_LENGTH]


def validate_actor_can_manage_group_join_code(
    *,
    actor,
    group: StudyGroup,
) -> None:
    """
    Проверяет право управления кодом вступления в группу.
    """

    if not actor_can_manage_study_group(
        actor=actor,
        group=group,
    ):
        raise PermissionDenied(
            "У пользователя нет прав управлять кодом этой группы."
        )


@transaction.atomic
def set_group_join_code(
    *,
    actor,
    group: StudyGroup,
    raw_code: str = "",
    expires_at=None,
) -> tuple[StudyGroup, str]:
    """
    Устанавливает код вступления в группу.

    Если raw_code не передан, генерирует новый код.
    Открытое значение возвращается только в момент установки.
    """

    validate_actor_can_manage_group_join_code(
        actor=actor,
        group=group,
    )

    code = raw_code.strip() if raw_code else generate_group_join_code()

    if len(code) < MIN_GROUP_JOIN_CODE_LENGTH:
        raise ValidationError(
            {
                "join_code": "Код вступления в группу короче минимальной длины.",
            }
        )

    group.set_join_code(
        code,
        expires_at=expires_at,
        save=True,
    )

    return group, code


@transaction.atomic
def disable_group_join_code(
    *,
    actor,
    group: StudyGroup,
) -> StudyGroup:
    """
    Отключает код вступления в группу.
    """

    validate_actor_can_manage_group_join_code(
        actor=actor,
        group=group,
    )

    if not group.join_code_is_active:
        raise ValidationError(
            {
                "join_code_is_active": "Код вступления в группу уже отключён.",
            }
        )

    group.disable_join_code(save=True)

    return group


@transaction.atomic
def clear_group_join_code(
    *,
    actor,
    group: StudyGroup,
) -> StudyGroup:
    """
    Полностью очищает код вступления в группу.
    """

    validate_actor_can_manage_group_join_code(
        actor=actor,
        group=group,
    )

    group.clear_join_code(save=True)

    return group


def verify_group_join_code(
    *,
    group: StudyGroup,
    raw_code: str,
) -> bool:
    """
    Проверяет код вступления в группу.
    """

    if group is None:
        return False

    return group.verify_join_code(raw_code)