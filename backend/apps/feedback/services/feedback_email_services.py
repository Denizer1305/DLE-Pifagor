from __future__ import annotations

import logging

from apps.feedback.constants import CONTACT_FEEDBACK_ADMIN_EMAIL
from apps.feedback.models import FeedbackAttachment, FeedbackRequest
from django.core.mail import EmailMultiAlternatives
from django.template.defaultfilters import linebreaksbr
from django.utils.html import escape

logger = logging.getLogger(__name__)


def send_feedback_admin_notification(feedback_request: FeedbackRequest) -> None:
    subject = f"Новое обращение в ЦОС «Пифагор» #{feedback_request.pk}"
    attachments = list(feedback_request.attachments.all())
    attachments_text = build_attachments_text(attachments)

    text_body = (
        f"Новое обращение #{feedback_request.pk}\n\n"
        f"Тема: {feedback_request.get_topic_display()}\n"
        f"Имя: {feedback_request.full_name}\n"
        f"Email: {feedback_request.email}\n"
        f"Телефон: {feedback_request.phone or 'не указан'}\n"
        "Организация: "
        f"{feedback_request.organization_name or 'не указана'}\n\n"
        f"Сообщение:\n{feedback_request.message}\n\n"
        f"Прикрепленные файлы:\n{attachments_text}\n\n"
    )

    email_message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=None,
        to=[CONTACT_FEEDBACK_ADMIN_EMAIL],
        reply_to=[feedback_request.email],
    )
    email_message.attach_alternative(
        build_feedback_admin_html(feedback_request, attachments),
        "text/html",
    )

    for attachment in attachments:
        try:
            attachment.file.open("rb")
            email_message.attach(
                filename=attachment.original_name,
                content=attachment.file.read(),
                mimetype=attachment.mime_type or None,
            )
        except OSError:
            logger.exception(
                "Failed to attach feedback file "
                "feedback_request_id=%s attachment_id=%s",
                feedback_request.pk,
                attachment.pk,
            )
        finally:
            try:
                attachment.file.close()
            except OSError:
                pass

    email_message.send(fail_silently=False)


def build_feedback_admin_html(
    feedback_request: FeedbackRequest,
    attachments: list[FeedbackAttachment],
) -> str:
    topic = escape(feedback_request.get_topic_display())
    full_name = escape(feedback_request.full_name)
    email = escape(feedback_request.email)
    phone = escape(feedback_request.phone or "не указан")
    organization = escape(feedback_request.organization_name or "не указана")
    subject = escape(feedback_request.subject or "Без темы")
    message = linebreaksbr(escape(feedback_request.message))
    attachments_html = build_attachments_html(attachments)

    return f"""
<!doctype html>
<html lang="ru">
  <body style="margin:0;background:#f4f7fb;padding:28px;font-family:Arial,sans-serif;color:#344158;">
    <table role="presentation" width="100%" cellspacing="0" cellpadding="0">
      <tr>
        <td align="center">
          <table role="presentation" width="640" cellspacing="0" cellpadding="0" style="max-width:640px;width:100%;background:#ffffff;border-radius:28px;overflow:hidden;border:1px solid #dce4f0;box-shadow:0 20px 60px rgba(30,45,70,.10);">
            <tr>
              <td style="padding:28px 32px;background:#344158;color:#ffffff;">
                <div style="font-size:13px;letter-spacing:.12em;text-transform:uppercase;opacity:.78;">ЦОС «Пифагор»</div>
                <h1 style="margin:10px 0 0;font-size:28px;line-height:1.2;font-weight:700;">Новое обращение</h1>
                <p style="margin:10px 0 0;color:#d9e3f2;font-size:15px;">Заявка #{feedback_request.pk} поступила через форму обратной связи.</p>
              </td>
            </tr>
            <tr>
              <td style="padding:28px 32px;">
                <span style="display:inline-block;padding:8px 12px;border-radius:999px;background:#edf3fb;color:#406aa8;font-size:13px;font-weight:700;">{topic}</span>
                <h2 style="margin:18px 0 8px;font-size:22px;line-height:1.25;color:#344158;">{subject}</h2>
                <p style="margin:0;color:#838aa3;font-size:15px;">Автор: <strong style="color:#344158;">{full_name}</strong></p>

                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="margin:22px 0;border-spacing:0 10px;">
                  <tr>
                    <td style="padding:14px;border-radius:16px;background:#f6f8fb;color:#838aa3;font-size:13px;">Email<br><strong style="display:block;margin-top:5px;color:#344158;font-size:15px;">{email}</strong></td>
                    <td style="width:10px;"></td>
                    <td style="padding:14px;border-radius:16px;background:#f6f8fb;color:#838aa3;font-size:13px;">Телефон<br><strong style="display:block;margin-top:5px;color:#344158;font-size:15px;">{phone}</strong></td>
                  </tr>
                  <tr>
                    <td colspan="3" style="padding:14px;border-radius:16px;background:#f6f8fb;color:#838aa3;font-size:13px;">Организация<br><strong style="display:block;margin-top:5px;color:#344158;font-size:15px;">{organization}</strong></td>
                  </tr>
                </table>

                <div style="padding:20px;border-radius:20px;background:#fbfcfe;border:1px solid #e3e9f2;">
                  <div style="margin-bottom:10px;color:#344158;font-size:16px;font-weight:700;">Сообщение</div>
                  <div style="color:#626b84;font-size:15px;line-height:1.7;">{message}</div>
                </div>

                <div style="margin-top:18px;padding:18px;border-radius:20px;background:#f6f8fb;">
                  <div style="margin-bottom:10px;color:#344158;font-size:16px;font-weight:700;">Вложения</div>
                  {attachments_html}
                </div>
              </td>
            </tr>
            <tr>
              <td style="padding:18px 32px;background:#f6f8fb;color:#838aa3;font-size:13px;">
                Письмо сформировано автоматически. Ответ можно отправить прямо на email пользователя.
              </td>
            </tr>
          </table>
        </td>
      </tr>
    </table>
  </body>
</html>
"""


def build_attachments_html(attachments: list[FeedbackAttachment]) -> str:
    if not attachments:
        return '<p style="margin:0;color:#838aa3;">Файлов нет.</p>'

    items = "".join(
        (
            '<li style="margin:8px 0;color:#626b84;">'
            f'<strong style="color:#344158;">{escape(attachment.original_name)}</strong>'
            f" · {format_attachment_size(attachment.file_size)}"
            "</li>"
        )
        for attachment in attachments
    )

    return f'<ul style="margin:0;padding-left:18px;">{items}</ul>'


def build_attachments_text(attachments: list[FeedbackAttachment]) -> str:
    if not attachments:
        return "нет"

    return "\n".join(
        f"- {attachment.original_name} ({format_attachment_size(attachment.file_size)})"
        for attachment in attachments
    )


def format_attachment_size(size: int) -> str:
    if size < 1024:
        return f"{size} Б"

    if size < 1024 * 1024:
        return f"{size / 1024:.1f} КБ"

    return f"{size / 1024 / 1024:.1f} МБ"
