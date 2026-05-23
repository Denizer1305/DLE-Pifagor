from __future__ import annotations

from datetime import timedelta

from apps.users.constants.audit import UserAuditAction
from apps.users.constants.lifecycle import UserStatus
from apps.users.services.audit_services import create_user_audit_log
from django.db import transaction
from django.utils import timezone


def activate_user(*, user, request=None):
    """
    Активирует пользователя.

    Args:
        user:
            Пользователь.
        request:
            HTTP-запрос.

    Returns:
        User: Обновлённый пользователь.
    """

    user.status = UserStatus.ACTIVE
    user.is_active = True
    user.save(update_fields=["status", "is_active", "updated_at"])

    return user


def block_user(*, user, actor=None, reason: str = "", request=None):
    """
    Блокирует пользователя.

    Args:
        user:
            Пользователь.
        actor:
            Пользователь, который выполнил блокировку.
        reason:
            Причина блокировки.
        request:
            HTTP-запрос.

    Returns:
        User: Заблокированный пользователь.
    """

    user.status = UserStatus.BLOCKED
    user.is_active = False
    user.save(update_fields=["status", "is_active", "updated_at"])

    create_user_audit_log(
        actor=actor,
        target_user=user,
        action=UserAuditAction.USER_BLOCKED,
        message=reason or "Пользователь заблокирован.",
        request=request,
    )

    return user


def archive_user(*, user, actor=None, reason: str = "", request=None):
    """
    Архивирует пользователя.

    Args:
        user:
            Пользователь.
        actor:
            Пользователь, который выполнил архивацию.
        reason:
            Причина архивации.
        request:
            HTTP-запрос.

    Returns:
        User: Архивированный пользователь.
    """

    user.status = UserStatus.ARCHIVED
    user.is_active = False
    user.archive(user=actor, reason=reason, save=False)
    user.save(
        update_fields=[
            "status",
            "is_active",
            "archived_at",
            "archived_by",
            "archive_reason",
            "updated_at",
        ]
    )

    create_user_audit_log(
        actor=actor,
        target_user=user,
        action=UserAuditAction.USER_ARCHIVED,
        message=reason or "Пользователь архивирован.",
        request=request,
    )

    return user


def schedule_user_deletion(
    *,
    user,
    actor=None,
    when=None,
    reason: str = "",
    request=None,
):
    """
    Планирует удаление или анонимизацию пользователя.

    Args:
        user:
            Пользователь.
        actor:
            Пользователь, который запланировал удаление.
        when:
            Дата и время удаления.
        reason:
            Причина.
        request:
            HTTP-запрос.

    Returns:
        User: Обновлённый пользователь.
    """

    deletion_time = when or (timezone.now() + timedelta(days=7))

    user.status = UserStatus.SCHEDULED_FOR_DELETION
    user.is_active = False
    user.scheduled_for_deletion_at = deletion_time
    user.save(
        update_fields=[
            "status",
            "is_active",
            "scheduled_for_deletion_at",
            "updated_at",
        ]
    )

    create_user_audit_log(
        actor=actor,
        target_user=user,
        action=UserAuditAction.USER_SCHEDULED_FOR_DELETION,
        message=reason or "Пользователь запланирован к удалению или анонимизации.",
        metadata={
            "scheduled_for_deletion_at": deletion_time.isoformat(),
        },
        request=request,
    )

    return user


def schedule_user_deletion_after_rejection(
    *,
    user,
    actor=None,
    reason: str = "",
    request=None,
):
    """
    Планирует удаление пользователя после отклонения заявки.

    Args:
        user:
            Пользователь.
        actor:
            Пользователь, отклонивший заявку.
        reason:
            Причина.
        request:
            HTTP-запрос.

    Returns:
        User: Обновлённый пользователь.
    """

    return schedule_user_deletion(
        user=user,
        actor=actor,
        when=timezone.now() + timedelta(days=7),
        reason=reason,
        request=request,
    )


@transaction.atomic
def anonymize_user(*, user, actor=None, reason: str = "", request=None):
    """
    Анонимизирует персональные данные пользователя.

    Важно:
        Физически пользователь не удаляется, чтобы не сломать журнал,
        оценки, задания, олимпиады и аудит.

    Args:
        user:
            Пользователь.
        actor:
            Пользователь или система, выполнившая анонимизацию.
        reason:
            Причина анонимизации.
        request:
            HTTP-запрос.

    Returns:
        User: Анонимизированный пользователь.
    """

    anonymized_email = f"anon-{user.id}-{timezone.now().timestamp()}@pifagor.local"
    anonymized_phone = f"+700000{str(user.id).zfill(5)[-5:]}"

    user.email = anonymized_email
    user.phone = anonymized_phone
    user.first_name = "Анонимизирован"
    user.last_name = "Пользователь"
    user.middle_name = ""
    user.birth_date = None
    user.status = UserStatus.ANONYMIZED
    user.is_active = False
    user.is_login_allowed = False
    user.is_email_verified = False
    user.is_phone_verified = False
    user.anonymized_at = timezone.now()
    user.set_unusable_password()
    user.save()

    create_user_audit_log(
        actor=actor,
        target_user=user,
        action=UserAuditAction.USER_ANONYMIZED,
        message=reason or "Пользователь анонимизирован.",
        request=request,
    )

    return user
