from __future__ import annotations

from typing import Any

ATTEMPT_MUTABLE_FIELDS = {
    "test",
    "test_id",
    "learner",
    "learner_id",
    "attempt_number",
    "status",
    "check_status",
    "started_at",
    "submitted_at",
    "auto_checked_at",
    "reviewed_at",
    "confirmed_at",
    "published_at",
    "auto_score",
    "teacher_score",
    "final_score",
    "auto_grade",
    "teacher_grade",
    "final_grade",
    "requires_manual_review",
    "is_confirmed_by_teacher",
    "is_visible_to_learner",
    "is_visible_to_guardian",
    "reviewer_teacher",
    "reviewer_teacher_id",
    "teacher_comment",
}


def apply_attempt_payload(
    *,
    attempt,
    data: dict[str, Any],
) -> None:
    """
    Применяет разрешённые поля к попытке теста.
    """

    for field_name, value in data.items():
        if field_name in ATTEMPT_MUTABLE_FIELDS:
            setattr(attempt, field_name, value)
