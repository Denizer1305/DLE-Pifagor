from __future__ import annotations

import logging

from django.db import transaction

from apps.feedback.models import FeedbackAttachment, FeedbackRequest
from apps.feedback.services.feedback_email_services import (
    send_feedback_admin_notification,
)
from apps.feedback.validators import (
    normalize_feedback_text,
    validate_feedback_attachment,
    validate_feedback_attachments_count,
)

logger = logging.getLogger(__name__)


def get_client_ip(request) -> str:
    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR", "")


def get_request_user_agent(request) -> str:
    return request.META.get("HTTP_USER_AGENT", "")


@transaction.atomic
def create_feedback_request(
    *,
    request,
    topic: str,
    full_name: str,
    email: str,
    phone: str = "",
    organization_name: str = "",
    subject: str = "",
    message: str,
    is_personal_data_consent: bool,
    source: str = FeedbackRequest.SourceChoices.CONTACTS_PAGE,
    page_url: str = "",
    frontend_route: str = "",
    error_code: str = "",
    error_details: str = "",
    files=None,
) -> FeedbackRequest:
    files = validate_feedback_attachments_count(files or [])

    user = request.user if request.user.is_authenticated else None

    feedback_request = FeedbackRequest.objects.create(
        user=user,
        topic=topic,
        source=source,
        status=FeedbackRequest.StatusChoices.NEW,
        full_name=normalize_feedback_text(full_name),
        email=normalize_feedback_text(email),
        phone=normalize_feedback_text(phone),
        organization_name=normalize_feedback_text(organization_name),
        subject=normalize_feedback_text(subject),
        message=(message or "").strip(),
        is_personal_data_consent=is_personal_data_consent,
        page_url=page_url,
        frontend_route=normalize_feedback_text(frontend_route),
        error_code=normalize_feedback_text(error_code),
        error_details=(error_details or "").strip(),
        ip_address=get_client_ip(request) or None,
        user_agent=get_request_user_agent(request),
    )

    for file_obj in files:
        validate_feedback_attachment(file_obj)

        FeedbackAttachment.objects.create(
            feedback_request=feedback_request,
            file=file_obj,
            original_name=getattr(file_obj, "name", ""),
            mime_type=getattr(file_obj, "content_type", "") or "",
            file_size=getattr(file_obj, "size", 0) or 0,
        )

    try:
        send_feedback_admin_notification(feedback_request)
    except Exception as error:
        logger.exception(
            "Failed to send feedback admin notification feedback_request_id=%s",
            feedback_request.pk,
        )
        feedback_request.admin_notification_sent = False
        feedback_request.admin_notification_error = str(error)
        feedback_request.save(
            update_fields=[
                "admin_notification_sent",
                "admin_notification_error",
                "updated_at",
            ]
        )
    else:
        feedback_request.admin_notification_sent = True
        feedback_request.admin_notification_error = ""
        feedback_request.save(
            update_fields=[
                "admin_notification_sent",
                "admin_notification_error",
                "updated_at",
            ]
        )

    return feedback_request