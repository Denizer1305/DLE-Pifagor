"""
Совместимый фасад email-задач users.

Файл оставлен для старых импортов:

    from apps.users.tasks.email_tasks import send_email_verification_task

Новая внутренняя структура лежит в apps.users.tasks.emails.
"""

from __future__ import annotations

from apps.users.tasks.emails import (
    send_account_anonymized_task,
    send_account_archived_task,
    send_account_blocked_task,
    send_account_contact_changed_task,
    send_account_restored_task,
    send_account_scheduled_for_deletion_task,
    send_account_unblocked_task,
    send_email_verification_task,
    send_guardian_link_approved_task,
    send_guardian_link_rejected_task,
    send_guardian_link_requested_task,
    send_guardian_registration_completed_task,
    send_join_request_approved_task,
    send_join_request_created_for_reviewer_task,
    send_join_request_rejected_task,
    send_learner_profile_required_task,
    send_password_changed_task,
    send_password_reset_task,
    send_teacher_registration_pending_task,
    send_user_roles_changed_task,
)

__all__ = [
    "send_account_anonymized_task",
    "send_account_archived_task",
    "send_account_blocked_task",
    "send_account_contact_changed_task",
    "send_account_restored_task",
    "send_account_scheduled_for_deletion_task",
    "send_account_unblocked_task",
    "send_email_verification_task",
    "send_guardian_link_approved_task",
    "send_guardian_link_rejected_task",
    "send_guardian_link_requested_task",
    "send_guardian_registration_completed_task",
    "send_join_request_approved_task",
    "send_join_request_created_for_reviewer_task",
    "send_join_request_rejected_task",
    "send_learner_profile_required_task",
    "send_password_changed_task",
    "send_teacher_registration_pending_task",
    "send_password_reset_task",
    "send_user_roles_changed_task",
]
