from __future__ import annotations

from apps.feedback.models import FeedbackRequest
from django.shortcuts import get_object_or_404


def update_feedback_status(*, request_id: int, status: str) -> FeedbackRequest:
    feedback_request = get_object_or_404(FeedbackRequest, pk=request_id)
    feedback_request.status = status
    feedback_request.save(update_fields=["status", "updated_at"])

    return feedback_request
