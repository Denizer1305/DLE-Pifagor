from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

"""
Email-слой приложения users.

Здесь используется ленивый импорт через __getattr__,
чтобы не создавать циклические импорты между:
    emails -> services -> tasks -> emails.

Можно импортировать так:
    from apps.users.emails import send_email_verification_email
"""


_EMAIL_EXPORTS = {
    "send_email_verification_email": "apps.users.emails.registration_emails",
    "send_teacher_registration_pending_email": "apps.users.emails.registration_emails",
    "send_learner_profile_required_email": "apps.users.emails.registration_emails",
    "send_guardian_registration_completed_email": "apps.users.emails.registration_emails",
    "send_join_request_approved_email": "apps.users.emails.join_request_emails",
    "send_join_request_rejected_email": "apps.users.emails.join_request_emails",
    "send_join_request_created_for_reviewer_email": "apps.users.emails.join_request_emails",
    "send_guardian_link_requested_email": "apps.users.emails.guardian_emails",
    "send_guardian_link_approved_email": "apps.users.emails.guardian_emails",
    "send_guardian_link_rejected_email": "apps.users.emails.guardian_emails",
    "send_account_blocked_email": "apps.users.emails.lifecycle_emails",
    "send_account_scheduled_for_deletion_email": "apps.users.emails.lifecycle_emails",
    "send_account_anonymized_email": "apps.users.emails.lifecycle_emails",
}


def __getattr__(name: str):
    """
    Лениво импортирует email-функцию при первом обращении.

    Args:
        name:
            Имя запрашиваемого атрибута.

    Returns:
        object: Запрошенная функция.

    Raises:
        AttributeError: Если имя не зарегистрировано в фасаде.
    """

    if name not in _EMAIL_EXPORTS:
        raise AttributeError(f"module 'apps.users.emails' has no attribute '{name}'")

    module = import_module(_EMAIL_EXPORTS[name])
    value = getattr(module, name)

    globals()[name] = value

    return value


def __dir__() -> list[str]:
    """
    Возвращает список публичных имён пакета.

    Returns:
        list[str]: Список экспортируемых имён.
    """

    return sorted(list(globals().keys()) + list(_EMAIL_EXPORTS.keys()))


if TYPE_CHECKING:
    from apps.users.emails.guardian_emails import (
        send_guardian_link_approved_email as send_guardian_link_approved_email,
    )
    from apps.users.emails.guardian_emails import (
        send_guardian_link_rejected_email as send_guardian_link_rejected_email,
    )
    from apps.users.emails.guardian_emails import (
        send_guardian_link_requested_email as send_guardian_link_requested_email,
    )
    from apps.users.emails.join_request_emails import (
        send_join_request_approved_email as send_join_request_approved_email,
    )
    from apps.users.emails.join_request_emails import (
        send_join_request_created_for_reviewer_email as send_join_request_created_for_reviewer_email,
    )
    from apps.users.emails.join_request_emails import (
        send_join_request_rejected_email as send_join_request_rejected_email,
    )
    from apps.users.emails.lifecycle_emails import (
        send_account_anonymized_email as send_account_anonymized_email,
    )
    from apps.users.emails.lifecycle_emails import (
        send_account_blocked_email as send_account_blocked_email,
    )
    from apps.users.emails.lifecycle_emails import (
        send_account_scheduled_for_deletion_email as send_account_scheduled_for_deletion_email,
    )
    from apps.users.emails.registration_emails import (
        send_email_verification_email as send_email_verification_email,
    )
    from apps.users.emails.registration_emails import (
        send_guardian_registration_completed_email as send_guardian_registration_completed_email,
    )
    from apps.users.emails.registration_emails import (
        send_learner_profile_required_email as send_learner_profile_required_email,
    )
    from apps.users.emails.registration_emails import (
        send_teacher_registration_pending_email as send_teacher_registration_pending_email,
    )


__all__ = list(_EMAIL_EXPORTS.keys())
