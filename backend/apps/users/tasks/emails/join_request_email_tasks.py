from __future__ import annotations

from apps.users.emails.join_request_emails import (
    send_join_request_approved_email,
    send_join_request_created_for_reviewer_email,
    send_join_request_rejected_email,
)
from apps.users.tasks.emails.helpers import send_user_email_or_retry
from celery import shared_task


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_join_request_approved_task(self, *, user_id: int) -> bool:
    """
    Отправляет письмо о подтверждении заявки пользователя.

    Args:
        user_id:
            ID пользователя.

    Returns:
        bool: True, если письмо отправлено.
    """

    return send_user_email_or_retry(
        self,
        user_id=user_id,
        email_sender=send_join_request_approved_email,
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_join_request_rejected_task(
    self,
    *,
    user_id: int,
    review_comment: str = "",
) -> bool:
    """
    Отправляет письмо об отклонении заявки пользователя.

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
        email_sender=send_join_request_rejected_email,
        review_comment=review_comment,
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_join_request_created_for_reviewer_task(
    self,
    *,
    reviewer_id: int,
    applicant_name: str = "",
    action_url: str = "/join-requests",
) -> bool:
    """
    Отправляет проверяющему письмо о новой заявке.

    Args:
        reviewer_id:
            ID проверяющего пользователя.
        applicant_name:
            Имя пользователя, подавшего заявку.
        action_url:
            Ссылка на заявку или раздел заявок.

    Returns:
        bool: True, если письмо отправлено.
    """

    return send_user_email_or_retry(
        self,
        user_id=reviewer_id,
        user_kwarg="reviewer",
        email_sender=send_join_request_created_for_reviewer_email,
        applicant_name=applicant_name,
        action_url=action_url,
    )
