from __future__ import annotations

from datetime import timedelta

from apps.users.constants.lifecycle import UserStatus
from apps.users.models import User
from apps.users.selectors.admin_user_selectors import actor_can_access_admin_user
from apps.users.services.admin_users.audit_services import (
    log_admin_user_scheduled_for_deletion,
)
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied, ValidationError

DEFAULT_ADMIN_USER_DELETION_DELAY_DAYS = 7
"""
Количество дней до удаления или анонимизации пользователя.

Физически пользователя сразу не удаляем, потому что на него могут ссылаться:
    - журнал;
    - задания;
    - курсы;
    - расписание;
    - аудит;
    - заявки.
"""


def validate_admin_can_delete_user(*, actor, target_user: User) -> None:
    """
    Проверяет, может ли администратор запланировать удаление пользователя.

    Args:
        actor:
            Администратор, который выполняет действие.
        target_user:
            Пользователь, которого планируют удалить.

    Raises:
        PermissionDenied: Если пользователь недоступен администратору.
        ValidationError: Если администратор пытается удалить самого себя.
    """

    if not actor_can_access_admin_user(actor=actor, target_user=target_user):
        raise PermissionDenied(
            "Пользователь не найден или недоступен для текущего администратора."
        )

    if actor and target_user and actor.id == target_user.id:
        raise ValidationError(
            {
                "user": (
                    "Администратор не может запланировать удаление "
                    "собственного аккаунта."
                )
            }
        )


def validate_user_can_be_scheduled_for_deletion(*, target_user: User) -> None:
    """
    Проверяет, можно ли запланировать пользователя к удалению.

    Args:
        target_user:
            Пользователь.

    Raises:
        ValidationError: Если пользователь уже удаляется или анонимизирован.
    """

    if target_user.status == UserStatus.ANONYMIZED or target_user.anonymized_at:
        raise ValidationError(
            {
                "status": "Нельзя удалить анонимизированного пользователя.",
            }
        )

    if (
        target_user.status == UserStatus.SCHEDULED_FOR_DELETION
        or target_user.scheduled_for_deletion_at
    ):
        raise ValidationError(
            {
                "status": "Пользователь уже запланирован к удалению.",
            }
        )


def get_admin_user_deletion_time(*, when=None):
    """
    Возвращает дату и время будущего удаления пользователя.

    Args:
        when:
            Явно переданная дата удаления.

    Returns:
        datetime: Дата и время удаления.
    """

    if when is not None:
        return when

    return timezone.now() + timedelta(days=DEFAULT_ADMIN_USER_DELETION_DELAY_DAYS)


def admin_schedule_user_deletion(
    *,
    actor,
    target_user: User,
    when=None,
    reason: str = "",
    bulk_action_id: str = "",
    request=None,
) -> User:
    """
    Планирует удаление или анонимизацию пользователя из админки.

    Важно:
        Метод не удаляет пользователя физически.
        Пользователь переводится в статус SCHEDULED_FOR_DELETION,
        а фактическое удаление или анонимизация должны выполняться отдельной
        фоновой задачей.

    Args:
        actor:
            Администратор, который выполняет действие.
        target_user:
            Пользователь, которого планируют удалить.
        when:
            Дата и время будущего удаления.
        reason:
            Причина удаления.
        bulk_action_id:
            ID массового действия.
        request:
            HTTP-запрос.

    Returns:
        User: Пользователь, запланированный к удалению.

    Raises:
        PermissionDenied: Если нет прав.
        ValidationError: Если действие невозможно.
    """

    validate_admin_can_delete_user(
        actor=actor,
        target_user=target_user,
    )
    validate_user_can_be_scheduled_for_deletion(target_user=target_user)

    scheduled_for_deletion_at = get_admin_user_deletion_time(when=when)

    target_user.status = UserStatus.SCHEDULED_FOR_DELETION
    target_user.is_active = False
    target_user.scheduled_for_deletion_at = scheduled_for_deletion_at
    target_user.save(
        update_fields=[
            "status",
            "is_active",
            "scheduled_for_deletion_at",
            "updated_at",
        ]
    )

    log_admin_user_scheduled_for_deletion(
        actor=actor,
        target_user=target_user,
        scheduled_for_deletion_at=scheduled_for_deletion_at,
        reason=reason,
        bulk_action_id=bulk_action_id,
        request=request,
    )

    return target_user
