from __future__ import annotations

from apps.feedback.models import FeedbackRequest
from django.db.models import Count, Q, QuerySet


def get_feedback_requests_queryset(
    *,
    status: str = "",
    topic: str = "",
    search: str = "",
) -> QuerySet[FeedbackRequest]:
    queryset = (
        FeedbackRequest.objects.annotate(
            attachment_count=Count("attachments"),
        )
        .prefetch_related("attachments")
        .order_by("-created_at")
    )

    if status:
        queryset = queryset.filter(status=status)

    if topic:
        queryset = queryset.filter(topic=topic)

    if search:
        queryset = queryset.filter(
            Q(full_name__icontains=search)
            | Q(email__icontains=search)
            | Q(subject__icontains=search)
            | Q(message__icontains=search)
        )

    return queryset


def get_feedback_summary_payload() -> dict[str, int]:
    counts = {
        item["status"]: item["count"]
        for item in FeedbackRequest.objects.values("status").annotate(count=Count("id"))
    }

    return {
        "total": FeedbackRequest.objects.count(),
        "new": counts.get(FeedbackRequest.StatusChoices.NEW, 0),
        "in_progress": counts.get(FeedbackRequest.StatusChoices.IN_PROGRESS, 0),
        "answered": counts.get(FeedbackRequest.StatusChoices.ANSWERED, 0),
        "closed": counts.get(FeedbackRequest.StatusChoices.CLOSED, 0),
    }
