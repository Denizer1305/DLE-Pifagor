from __future__ import annotations

from apps.users.emails.security_emails import (
    send_account_contact_changed_email,
    send_password_changed_email,
    send_user_roles_changed_email,
)
from apps.users.tasks.emails.helpers import send_user_email_or_retry
from celery import shared_task


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_password_changed_task(self, *, user_id: int) -> bool:
    return send_user_email_or_retry(
        self,
        user_id=user_id,
        email_sender=send_password_changed_email,
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_account_contact_changed_task(
    self,
    *,
    user_id: int,
    changed_fields: str = "",
) -> bool:
    return send_user_email_or_retry(
        self,
        user_id=user_id,
        email_sender=send_account_contact_changed_email,
        changed_fields=changed_fields,
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_user_roles_changed_task(
    self,
    *,
    user_id: int,
    assigned_roles_text: str = "",
    revoked_roles_text: str = "",
) -> bool:
    return send_user_email_or_retry(
        self,
        user_id=user_id,
        email_sender=send_user_roles_changed_email,
        assigned_roles_text=assigned_roles_text,
        revoked_roles_text=revoked_roles_text,
    )
