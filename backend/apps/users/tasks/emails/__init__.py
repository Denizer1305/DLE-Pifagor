from __future__ import annotations

from apps.users.tasks.emails.guardian_email_tasks import (
    send_guardian_link_approved_task,
    send_guardian_link_rejected_task,
    send_guardian_link_requested_task,
)
from apps.users.tasks.emails.join_request_email_tasks import (
    send_join_request_approved_task,
    send_join_request_created_for_reviewer_task,
    send_join_request_rejected_task,
)
from apps.users.tasks.emails.lifecycle_email_tasks import (
    send_account_anonymized_task,
    send_account_blocked_task,
    send_account_scheduled_for_deletion_task,
)
from apps.users.tasks.emails.registration_email_tasks import (
    send_email_verification_task,
    send_guardian_registration_completed_task,
    send_learner_profile_required_task,
    send_password_reset_task,
    send_teacher_registration_pending_task,
)

__all__ = [
    "send_account_anonymized_task",
    "send_account_blocked_task",
    "send_account_scheduled_for_deletion_task",
    "send_email_verification_task",
    "send_guardian_link_approved_task",
    "send_guardian_link_rejected_task",
    "send_guardian_link_requested_task",
    "send_guardian_registration_completed_task",
    "send_join_request_approved_task",
    "send_join_request_created_for_reviewer_task",
    "send_join_request_rejected_task",
    "send_learner_profile_required_task",
    "send_teacher_registration_pending_task",
]
