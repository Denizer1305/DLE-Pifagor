from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING

"""
Фоновые задачи приложения users.

Здесь используется ленивый импорт, чтобы tasks не создавали циклические
зависимости с emails и services.

Можно импортировать так:
    from apps.users.tasks import send_email_verification_task
"""


_TASK_EXPORTS = {
    "cleanup_unused_expired_invite_codes_task": "apps.users.tasks.cleanup_tasks",
    "deactivate_expired_invite_codes_task": "apps.users.tasks.cleanup_tasks",
    "expire_old_join_requests_task": "apps.users.tasks.cleanup_tasks",
    "send_account_anonymized_task": "apps.users.tasks.email_tasks",
    "send_account_blocked_task": "apps.users.tasks.email_tasks",
    "send_account_scheduled_for_deletion_task": "apps.users.tasks.email_tasks",
    "send_email_verification_task": "apps.users.tasks.email_tasks",
    "send_guardian_link_approved_task": "apps.users.tasks.email_tasks",
    "send_guardian_link_rejected_task": "apps.users.tasks.email_tasks",
    "send_guardian_link_requested_task": "apps.users.tasks.email_tasks",
    "send_guardian_registration_completed_task": "apps.users.tasks.email_tasks",
    "send_join_request_approved_task": "apps.users.tasks.email_tasks",
    "send_join_request_created_for_reviewer_task": "apps.users.tasks.email_tasks",
    "send_join_request_rejected_task": "apps.users.tasks.email_tasks",
    "send_learner_profile_required_task": "apps.users.tasks.email_tasks",
    "send_teacher_registration_pending_task": "apps.users.tasks.email_tasks",
    "anonymize_scheduled_users_task": "apps.users.tasks.lifecycle_tasks",
    "archive_inactive_rejected_users_task": "apps.users.tasks.lifecycle_tasks",
}


def __getattr__(name: str):
    """
    Лениво импортирует задачу при первом обращении.

    Args:
        name:
            Имя запрашиваемой задачи.

    Returns:
        object: Celery task.

    Raises:
        AttributeError: Если имя не зарегистрировано в фасаде.
    """

    if name not in _TASK_EXPORTS:
        raise AttributeError(f"module 'apps.users.tasks' has no attribute '{name}'")

    module = import_module(_TASK_EXPORTS[name])
    value = getattr(module, name)

    globals()[name] = value

    return value


def __dir__() -> list[str]:
    """
    Возвращает список публичных имён пакета.

    Returns:
        list[str]: Список экспортируемых задач.
    """

    return sorted(list(globals().keys()) + list(_TASK_EXPORTS.keys()))


if TYPE_CHECKING:
    from apps.users.tasks.cleanup_tasks import (
        cleanup_unused_expired_invite_codes_task,
        deactivate_expired_invite_codes_task,
        expire_old_join_requests_task,
    )
    from apps.users.tasks.email_tasks import (
        send_account_anonymized_task,
        send_account_blocked_task,
        send_account_scheduled_for_deletion_task,
        send_email_verification_task,
        send_guardian_link_approved_task,
        send_guardian_link_rejected_task,
        send_guardian_link_requested_task,
        send_guardian_registration_completed_task,
        send_join_request_approved_task,
        send_join_request_created_for_reviewer_task,
        send_join_request_rejected_task,
        send_learner_profile_required_task,
        send_teacher_registration_pending_task,
    )
    from apps.users.tasks.lifecycle_tasks import (
        anonymize_scheduled_users_task,
        archive_inactive_rejected_users_task,
    )


__all__ = list(_TASK_EXPORTS.keys())
