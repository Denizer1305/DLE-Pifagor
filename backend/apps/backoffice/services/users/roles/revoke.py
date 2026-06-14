from __future__ import annotations

from apps.backoffice.services.users.roles.queries import (
    get_backoffice_user_role_for_revoke,
)
from apps.backoffice.services.users.roles.validation import (
    validate_actor_can_revoke_backoffice_user_role,
)
from apps.users.constants.lifecycle import UserRoleStatus
from apps.users.models import User, UserRole
from rest_framework.exceptions import ValidationError


def revoke_backoffice_user_role_by_id(
    *,
    actor,
    target_user: User,
    user_role_id: int,
    reason: str = "",
) -> UserRole:
    """
    Отзывает назначенную роль пользователя по ID.
    """

    user_role = get_backoffice_user_role_for_revoke(
        target_user=target_user,
        user_role_id=user_role_id,
    )

    if user_role is None:
        raise ValidationError(
            {
                "revoked_user_role_ids": "Назначенная роль пользователя не найдена.",
            }
        )

    if user_role.status == UserRoleStatus.REVOKED:
        raise ValidationError(
            {
                "revoked_user_role_ids": "Роль пользователя уже отозвана.",
            }
        )

    validate_actor_can_revoke_backoffice_user_role(
        actor=actor,
        user_role=user_role,
    )

    user_role.revoke(
        user=actor,
        reason=reason,
        save=True,
    )

    return user_role


# Совместимый alias.
revoke_user_role_by_id = revoke_backoffice_user_role_by_id
