from __future__ import annotations

import logging

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.feedback.constants import CONTACT_FEEDBACK_ADMIN_EMAIL
from apps.feedback.models import FeedbackRequest

logger = logging.getLogger(__name__)


def send_feedback_admin_notification(feedback_request: FeedbackRequest) -> None:
    subject = f"Новое обращение в ЦОС «Пифагор» #{feedback_request.pk}"

    text_body = (
        f"Новое обращение #{feedback_request.pk}\n\n"
        f"Тема: {feedback_request.get_topic_display()}\n"
        f"Имя: {feedback_request.full_name}\n"
        f"Email: {feedback_request.email}\n"
        f"Телефон: {feedback_request.phone or 'не указан'}\n"
        f"Организация: {feedback_request.organization_name or 'не указана'}\n\n"
        f"Сообщение:\n{feedback_request.message}\n\n"
        f"Источник: {feedback_request.get_source_display()}\n"
        f"Страница: {feedback_request.page_url or 'не указана'}\n"
        f"IP: {feedback_request.ip_address or 'не определён'}\n"
    )

    email_message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=None,
        to=[CONTACT_FEEDBACK_ADMIN_EMAIL],
        reply_to=[feedback_request.email],
    )

    for attachment in feedback_request.attachments.all():
        try:
            attachment.file.open("rb")
            email_message.attach(
                filename=attachment.original_name,
                content=attachment.file.read(),
                mimetype=attachment.mime_type or None,
            )
        except OSError:
            logger.exception(
                "Failed to attach feedback file feedback_request_id=%s attachment_id=%s",
                feedback_request.pk,
                attachment.pk,
            )
        finally:
            try:
                attachment.file.close()
            except OSError:
                pass

    email_message.send(fail_silently=False)