from __future__ import annotations

from apps.users.emails.registration_emails import (
    send_email_verification_email,
    send_guardian_registration_completed_email,
    send_learner_profile_required_email,
    send_password_reset_email,
    send_teacher_registration_pending_email,
)
from apps.users.tasks.emails.helpers import send_user_email_or_retry
from celery import shared_task


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_email_verification_task(self, *, user_id: int) -> bool:
    """
    Отправляет письмо подтверждения email.

    Args:
        user_id:
            ID пользователя.

    Returns:
        bool: True, если письмо отправлено или уже не требуется.
    """

    return send_user_email_or_retry(
        self,
        user_id=user_id,
        email_sender=send_email_verification_email,
        skip_if_email_verified=True,
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_teacher_registration_pending_task(self, *, user_id: int) -> bool:
    """
    Отправляет преподавателю письмо о том, что заявка ушла администратору.

    Args:
        user_id:
            ID пользователя преподавателя.

    Returns:
        bool: True, если письмо отправлено.
    """

    return send_user_email_or_retry(
        self,
        user_id=user_id,
        email_sender=send_teacher_registration_pending_email,
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_learner_profile_required_task(self, *, user_id: int) -> bool:
    """
    Отправляет учащемуся письмо о необходимости завершить настройку профиля.

    Args:
        user_id:
            ID пользователя учащегося.

    Returns:
        bool: True, если письмо отправлено.
    """

    return send_user_email_or_retry(
        self,
        user_id=user_id,
        email_sender=send_learner_profile_required_email,
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_guardian_registration_completed_task(self, *, user_id: int) -> bool:
    """
    Отправляет родителю письмо после завершения регистрации.

    Args:
        user_id:
            ID пользователя родителя.

    Returns:
        bool: True, если письмо отправлено.
    """

    return send_user_email_or_retry(
        self,
        user_id=user_id,
        email_sender=send_guardian_registration_completed_email,
    )


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_password_reset_task(self, *, user_id: int) -> bool:
    """
    Отправляет письмо восстановления пароля.

    Args:
        user_id:
            ID пользователя.

    Returns:
        bool: True, если письмо отправлено.
    """

    return send_user_email_or_retry(
        self,
        user_id=user_id,
        email_sender=send_password_reset_email,
    )
