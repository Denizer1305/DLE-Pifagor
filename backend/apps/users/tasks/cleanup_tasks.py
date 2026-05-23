from __future__ import annotations

from apps.users.constants.onboarding import JoinRequestStatus
from apps.users.models import InviteCode, UserJoinRequest
from celery import shared_task
from django.utils import timezone


@shared_task
def deactivate_expired_invite_codes_task() -> int:
    """
    Деактивирует истёкшие коды приглашения.

    Returns:
        int: Количество отключённых кодов.
    """

    now = timezone.now()

    updated_count = InviteCode.objects.filter(
        is_active=True,
        expires_at__lte=now,
    ).update(
        is_active=False,
        updated_at=now,
    )

    return updated_count


@shared_task
def expire_old_join_requests_task() -> int:
    """
    Помечает истёкшие заявки пользователей как expired.

    Обрабатываются только заявки:
        - со статусом pending;
        - с заполненным expires_at;
        - у которых expires_at уже наступил.

    Returns:
        int: Количество истёкших заявок.
    """

    now = timezone.now()

    updated_count = UserJoinRequest.objects.filter(
        status=JoinRequestStatus.PENDING,
        expires_at__isnull=False,
        expires_at__lte=now,
    ).update(
        status=JoinRequestStatus.EXPIRED,
        updated_at=now,
    )

    return updated_count


@shared_task
def cleanup_unused_expired_invite_codes_task(*, days: int = 30) -> int:
    """
    Удаляет старые неиспользованные истёкшие коды приглашения.

    Args:
        days:
            Через сколько дней после истечения код можно удалить.

    Returns:
        int: Количество удалённых кодов.
    """

    threshold = timezone.now() - timezone.timedelta(days=days)

    deleted_count, _details = InviteCode.objects.filter(
        is_active=False,
        used_count=0,
        expires_at__lte=threshold,
    ).delete()

    return deleted_count
