from __future__ import annotations

from apps.users.emails.guardian_emails import (
    send_guardian_link_approved_email,
    send_guardian_link_rejected_email,
    send_guardian_link_requested_email,
)
from apps.users.tasks.emails.helpers import send_user_email_or_retry
from celery import shared_task


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_guardian_link_requested_task(self, *, user_id: int) -> bool:
    """
    Отправляет письмо о создании запроса связи родителя и учащегося.

    Args:
        user_id:
            ID пользователя.

    Returns:
        bool: True, если письмо отправлено.
    """

    return send_user_email_or_retry(
        self,
        user_id=user_id,
        email_sender=send_guardian_link_requested_email,
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_guardian_link_approved_task(self, *, user_id: int) -> bool:
    """
    Отправляет письмо о подтверждении связи родителя и учащегося.

    Args:
        user_id:
            ID пользователя.

    Returns:
        bool: True, если письмо отправлено.
    """

    return send_user_email_or_retry(
        self,
        user_id=user_id,
        email_sender=send_guardian_link_approved_email,
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_guardian_link_rejected_task(
    self,
    *,
    user_id: int,
    review_comment: str = "",
) -> bool:
    """
    Отправляет письмо об отклонении связи родителя и учащегося.

    Args:
        user_id:
            ID пользователя.
        review_comment:
            Комментарий проверяющего.

    Returns:
        bool: True, если письмо отправлено.
    """

    return send_user_email_or_retry(
        self,
        user_id=user_id,
        email_sender=send_guardian_link_rejected_email,
        review_comment=review_comment,
    )
