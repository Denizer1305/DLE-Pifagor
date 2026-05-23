from __future__ import annotations

from apps.users.constants.audit import AuditActorType
from apps.users.constants.lifecycle import UserStatus
from apps.users.models import User
from apps.users.services.audit_services import create_user_audit_log
from apps.users.services.user_lifecycle_services import anonymize_user
from celery import shared_task
from django.utils import timezone


@shared_task
def anonymize_scheduled_users_task() -> int:
    """
    Анонимизирует пользователей, у которых наступила дата удаления.

    Пользователь физически не удаляется из базы, чтобы не ломать:
        - журнал;
        - задания;
        - оценки;
        - заявки;
        - аудит;
        - историю участия в олимпиадах.

    Returns:
        int: Количество анонимизированных пользователей.
    """

    now = timezone.now()

    users_queryset = User.objects.filter(
        status=UserStatus.SCHEDULED_FOR_DELETION,
        scheduled_for_deletion_at__isnull=False,
        scheduled_for_deletion_at__lte=now,
    )

    anonymized_count = 0

    for user in users_queryset.iterator():
        anonymize_user(
            user=user,
            actor=None,
            reason="Автоматическая анонимизация по истечении срока ожидания.",
            request=None,
        )
        anonymized_count += 1

    return anonymized_count


@shared_task
def archive_inactive_rejected_users_task() -> int:
    """
    Архивирует отклонённых пользователей, если они ещё не запланированы к удалению.

    Эта задача нужна как страховка, чтобы отклонённые аккаунты
    не оставались в промежуточном состоянии без дальнейшего lifecycle.

    Returns:
        int: Количество обработанных пользователей.
    """

    users_queryset = User.objects.filter(
        status=UserStatus.REJECTED,
        scheduled_for_deletion_at__isnull=True,
    )

    processed_count = 0

    for user in users_queryset.iterator():
        user.status = UserStatus.ARCHIVED
        user.is_active = False
        user.save(update_fields=["status", "is_active", "updated_at"])

        create_user_audit_log(
            action="user_archived",
            actor=None,
            actor_type=AuditActorType.SYSTEM,
            target_user=user,
            message="Пользователь автоматически архивирован после отклонения.",
            request=None,
        )

        processed_count += 1

    return processed_count
