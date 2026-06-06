from __future__ import annotations

from apps.users.emails.lifecycle_emails import (
    send_account_anonymized_email,
    send_account_archived_email,
    send_account_blocked_email,
    send_account_restored_email,
    send_account_scheduled_for_deletion_email,
    send_account_unblocked_email,
)
from apps.users.tasks.emails.helpers import send_user_email_or_retry
from celery import shared_task


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_account_blocked_task(
    self,
    *,
    user_id: int,
    reason: str = "",
) -> bool:
    """
    Отправляет письмо о блокировке аккаунта.

    Args:
        user_id:
            ID пользователя.
        reason:
            Причина блокировки.

    Returns:
        bool: True, если письмо отправлено.
    """

    return send_user_email_or_retry(
        self,
        user_id=user_id,
        email_sender=send_account_blocked_email,
        reason=reason,
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_account_scheduled_for_deletion_task(
    self,
    *,
    user_id: int,
    scheduled_for_deletion_at: str = "",
) -> bool:
    """
    Отправляет письмо о запланированной анонимизации аккаунта.

    Args:
        user_id:
            ID пользователя.
        scheduled_for_deletion_at:
            Дата и время планируемой анонимизации.

    Returns:
        bool: True, если письмо отправлено.
    """

    return send_user_email_or_retry(
        self,
        user_id=user_id,
        email_sender=send_account_scheduled_for_deletion_email,
        scheduled_for_deletion_at=scheduled_for_deletion_at,
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_account_anonymized_task(self, *, user_id: int) -> bool:
    """
    Отправляет письмо об анонимизации аккаунта.

    Args:
        user_id:
            ID пользователя.

    Returns:
        bool: True, если письмо отправлено.
    """

    return send_user_email_or_retry(
        self,
        user_id=user_id,
        email_sender=send_account_anonymized_email,
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_account_unblocked_task(
    self,
    *,
    user_id: int,
    reason: str = "",
) -> bool:
    return send_user_email_or_retry(
        self,
        user_id=user_id,
        email_sender=send_account_unblocked_email,
        reason=reason,
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_account_archived_task(
    self,
    *,
    user_id: int,
    reason: str = "",
) -> bool:
    return send_user_email_or_retry(
        self,
        user_id=user_id,
        email_sender=send_account_archived_email,
        reason=reason,
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_account_restored_task(
    self,
    *,
    user_id: int,
    previous_status: str = "",
    reason: str = "",
) -> bool:
    return send_user_email_or_retry(
        self,
        user_id=user_id,
        email_sender=send_account_restored_email,
        previous_status=previous_status,
        reason=reason,
    )
