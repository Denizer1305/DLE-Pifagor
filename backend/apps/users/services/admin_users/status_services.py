from __future__ import annotations

from apps.users.constants.lifecycle import UserStatus
from apps.users.models import User
from apps.users.selectors.admin_user_selectors import actor_can_access_admin_user
from apps.users.services.admin_users.audit_services import (
    log_admin_user_archived,
    log_admin_user_blocked,
    log_admin_user_restored,
    log_admin_user_unblocked,
)
from rest_framework.exceptions import PermissionDenied, ValidationError


def validate_admin_can_manage_user_status(*, actor, target_user: User) -> None:
    """
    Проверяет, может ли администратор менять статус пользователя.

    Args:
        actor:
            Администратор, который выполняет действие.
        target_user:
            Пользователь, чей статус меняется.

    Raises:
        PermissionDenied: Если пользователь недоступен администратору.
        ValidationError: Если администратор пытается изменить самого себя.
    """

    if not actor_can_access_admin_user(actor=actor, target_user=target_user):
        raise PermissionDenied(
            "Пользователь не найден или недоступен для текущего администратора."
        )

    if actor and target_user and actor.id == target_user.id:
        raise ValidationError(
            {
                "user": (
                    "Администратор не может менять собственный статус "
                    "через административное управление пользователями."
                )
            }
        )


def validate_user_status_is_not_final(*, target_user: User) -> None:
    """
    Проверяет, что пользователь не находится в финальном состоянии.

    Args:
        target_user:
            Пользователь.

    Raises:
        ValidationError: Если пользователь анонимизирован.
    """

    if target_user.status == UserStatus.ANONYMIZED or target_user.anonymized_at:
        raise ValidationError(
            {
                "status": "Нельзя изменить статус анонимизированного пользователя.",
            }
        )


def validate_user_is_not_scheduled_for_deletion(*, target_user: User) -> None:
    """
    Проверяет, что пользователь не запланирован к удалению.

    Args:
        target_user:
            Пользователь.

    Raises:
        ValidationError: Если пользователь уже запланирован к удалению.
    """

    if (
        target_user.status == UserStatus.SCHEDULED_FOR_DELETION
        or target_user.scheduled_for_deletion_at
    ):
        raise ValidationError(
            {
                "status": (
                    "Пользователь уже запланирован к удалению. "
                    "Сначала восстановите пользователя."
                )
            }
        )


def get_restored_user_status(*, target_user: User) -> str:
    """
    Определяет статус пользователя после восстановления.

    Если email не подтверждён, пользователь возвращается в ожидание
    подтверждения email. Если email подтверждён, пользователь становится активным.

    Args:
        target_user:
            Восстанавливаемый пользователь.

    Returns:
        str: Новый статус пользователя.
    """

    if not target_user.is_email_verified:
        return UserStatus.PENDING_EMAIL

    return UserStatus.ACTIVE


def admin_block_user(
    *,
    actor,
    target_user: User,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
) -> User:
    """
    Блокирует пользователя из административного раздела.

    Args:
        actor:
            Администратор, который выполняет блокировку.
        target_user:
            Блокируемый пользователь.
        reason:
            Причина блокировки.
        bulk_action_id:
            ID массового действия.
        request:
            HTTP-запрос.

    Returns:
        User: Заблокированный пользователь.

    Raises:
        PermissionDenied: Если нет прав.
        ValidationError: Если действие невозможно.
    """

    validate_admin_can_manage_user_status(
        actor=actor,
        target_user=target_user,
    )
    validate_user_status_is_not_final(target_user=target_user)
    validate_user_is_not_scheduled_for_deletion(target_user=target_user)

    if target_user.status == UserStatus.BLOCKED:
        raise ValidationError(
            {
                "status": "Пользователь уже заблокирован.",
            }
        )

    target_user.status = UserStatus.BLOCKED
    target_user.is_active = False
    target_user.save(
        update_fields=[
            "status",
            "is_active",
            "updated_at",
        ]
    )

    log_admin_user_blocked(
        actor=actor,
        target_user=target_user,
        reason=reason,
        bulk_action_id=bulk_action_id,
        request=request,
    )

    return target_user


def admin_unblock_user(
    *,
    actor,
    target_user: User,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
) -> User:
    """
    Разблокирует пользователя из административного раздела.

    Args:
        actor:
            Администратор, который выполняет разблокировку.
        target_user:
            Разблокируемый пользователь.
        reason:
            Причина разблокировки.
        bulk_action_id:
            ID массового действия.
        request:
            HTTP-запрос.

    Returns:
        User: Разблокированный пользователь.

    Raises:
        PermissionDenied: Если нет прав.
        ValidationError: Если действие невозможно.
    """

    validate_admin_can_manage_user_status(
        actor=actor,
        target_user=target_user,
    )
    validate_user_status_is_not_final(target_user=target_user)
    validate_user_is_not_scheduled_for_deletion(target_user=target_user)

    if target_user.status != UserStatus.BLOCKED:
        raise ValidationError(
            {
                "status": "Разблокировать можно только заблокированного пользователя.",
            }
        )

    target_user.status = get_restored_user_status(target_user=target_user)
    target_user.is_active = target_user.status == UserStatus.ACTIVE
    target_user.save(
        update_fields=[
            "status",
            "is_active",
            "updated_at",
        ]
    )

    log_admin_user_unblocked(
        actor=actor,
        target_user=target_user,
        reason=reason,
        bulk_action_id=bulk_action_id,
        request=request,
    )

    return target_user


def admin_archive_user(
    *,
    actor,
    target_user: User,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
) -> User:
    """
    Архивирует пользователя из административного раздела.

    Args:
        actor:
            Администратор, который выполняет архивацию.
        target_user:
            Архивируемый пользователь.
        reason:
            Причина архивации.
        bulk_action_id:
            ID массового действия.
        request:
            HTTP-запрос.

    Returns:
        User: Архивированный пользователь.

    Raises:
        PermissionDenied: Если нет прав.
        ValidationError: Если действие невозможно.
    """

    validate_admin_can_manage_user_status(
        actor=actor,
        target_user=target_user,
    )
    validate_user_status_is_not_final(target_user=target_user)
    validate_user_is_not_scheduled_for_deletion(target_user=target_user)

    if target_user.status == UserStatus.ARCHIVED:
        raise ValidationError(
            {
                "status": "Пользователь уже находится в архиве.",
            }
        )

    target_user.status = UserStatus.ARCHIVED
    target_user.is_active = False

    if hasattr(target_user, "archive"):
        target_user.archive(
            user=actor,
            reason=reason,
            save=False,
        )

    target_user.save(
        update_fields=[
            "status",
            "is_active",
            "archived_at",
            "archived_by",
            "archive_reason",
            "updated_at",
        ]
    )

    log_admin_user_archived(
        actor=actor,
        target_user=target_user,
        reason=reason,
        bulk_action_id=bulk_action_id,
        request=request,
    )

    return target_user


def admin_restore_user(
    *,
    actor,
    target_user: User,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
) -> User:
    """
    Восстанавливает пользователя из архива, блокировки или запланированного удаления.

    Args:
        actor:
            Администратор, который выполняет восстановление.
        target_user:
            Восстанавливаемый пользователь.
        reason:
            Причина восстановления.
        bulk_action_id:
            ID массового действия.
        request:
            HTTP-запрос.

    Returns:
        User: Восстановленный пользователь.

    Raises:
        PermissionDenied: Если нет прав.
        ValidationError: Если действие невозможно.
    """

    validate_admin_can_manage_user_status(
        actor=actor,
        target_user=target_user,
    )
    validate_user_status_is_not_final(target_user=target_user)

    previous_status = target_user.status

    allowed_statuses = {
        UserStatus.BLOCKED,
        UserStatus.ARCHIVED,
        UserStatus.SCHEDULED_FOR_DELETION,
    }

    if (
        previous_status not in allowed_statuses
        and not target_user.scheduled_for_deletion_at
    ):
        raise ValidationError(
            {
                "status": (
                    "Восстановить можно только заблокированного, архивного "
                    "или запланированного к удалению пользователя."
                )
            }
        )

    target_user.status = get_restored_user_status(target_user=target_user)
    target_user.is_active = target_user.status == UserStatus.ACTIVE
    target_user.scheduled_for_deletion_at = None

    update_fields = [
        "status",
        "is_active",
        "scheduled_for_deletion_at",
        "updated_at",
    ]

    if hasattr(target_user, "archived_at"):
        target_user.archived_at = None
        update_fields.append("archived_at")

    if hasattr(target_user, "archived_by"):
        target_user.archived_by = None
        update_fields.append("archived_by")

    if hasattr(target_user, "archive_reason"):
        target_user.archive_reason = ""
        update_fields.append("archive_reason")

    target_user.save(update_fields=update_fields)

    log_admin_user_restored(
        actor=actor,
        target_user=target_user,
        previous_status=previous_status,
        reason=reason,
        bulk_action_id=bulk_action_id,
        request=request,
    )

    return target_user
