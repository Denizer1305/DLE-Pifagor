from __future__ import annotations

from apps.backoffice.services.users.roles.payloads import (
    BackofficeRoleAssignmentPayload,
)
from apps.backoffice.services.users.roles.queries import (
    get_existing_backoffice_user_role_for_assignment,
)
from apps.core.services import save_model
from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.models import Role, User, UserRole
from django.db import IntegrityError
from django.utils import timezone
from rest_framework.exceptions import ValidationError


def create_or_restore_backoffice_user_role(
    *,
    actor,
    target_user: User,
    role: Role,
    payload: BackofficeRoleAssignmentPayload,
    reason: str = "",
) -> UserRole:
    """
    Создаёт или повторно активирует роль пользователя.

    Если такая роль уже была отозвана, отклонена или архивирована,
    она не создаётся повторно, а переводится в ACTIVE.
    """

    existing_user_role = get_existing_backoffice_user_role_for_assignment(
        target_user=target_user,
        role=role,
        payload=payload,
    )

    if existing_user_role:
        if existing_user_role.status == UserRoleStatus.ACTIVE:
            raise ValidationError(
                {
                    "role": "У пользователя уже есть такая активная роль.",
                }
            )

        existing_user_role.status = UserRoleStatus.ACTIVE
        existing_user_role.assigned_by = actor
        existing_user_role.assigned_at = timezone.now()
        existing_user_role.revoked_by = None
        existing_user_role.revoked_at = None
        existing_user_role.revoke_reason = ""

        save_model(
            existing_user_role,
            update_fields=[
                "status",
                "assigned_by",
                "assigned_at",
                "revoked_by",
                "revoked_at",
                "revoke_reason",
            ],
        )

        return existing_user_role

    try:
        return UserRole.objects.create(
            user=target_user,
            role=role,
            organization_id=payload.organization_id,
            department_id=payload.department_id,
            group_id=payload.group_id,
            status=UserRoleStatus.ACTIVE,
            assigned_by=actor,
            assigned_at=timezone.now(),
        )
    except IntegrityError as error:
        raise ValidationError(
            {
                "role": (
                    "Не удалось назначить роль. Возможно, такая роль уже "
                    "существует в этом контексте."
                )
            }
        ) from error


# Совместимый alias.
create_or_restore_user_role = create_or_restore_backoffice_user_role
