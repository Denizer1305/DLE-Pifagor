from __future__ import annotations

from apps.users.emails.base_email import send_templated_email
from apps.users.emails.email_context import get_base_email_context


def send_feedback_received_email(
    *,
    to_email: str,
    full_name: str = "",
    request_number: str = "",
) -> int:
    context = get_base_email_context(
        title="Обращение принято",
        preview_text="Мы получили ваше обращение в ЦОС «Пифагор».",
        action_url="/feedback",
        action_label="Открыть обратную связь",
        extra_context={
            "full_name": full_name,
            "request_number": request_number,
        },
    )

    return send_templated_email(
        subject="Обращение в ЦОС «Пифагор» принято",
        to_email=to_email,
        template_base="emails/feedback/received",
        context=context,
    )


def send_feedback_status_changed_email(
    *,
    to_email: str,
    status_label: str,
    request_number: str = "",
) -> int:
    context = get_base_email_context(
        title="Статус обращения изменён",
        preview_text="Статус вашего обращения в ЦОС «Пифагор» изменился.",
        action_url="/feedback",
        action_label="Открыть обратную связь",
        extra_context={
            "status_label": status_label,
            "request_number": request_number,
        },
    )

    return send_templated_email(
        subject="Статус обращения изменён",
        to_email=to_email,
        template_base="emails/feedback/status_changed",
        context=context,
    )


def send_feedback_answered_email(
    *,
    to_email: str,
    answer_text: str,
    request_number: str = "",
) -> int:
    context = get_base_email_context(
        title="На обращение ответили",
        preview_text="По вашему обращению в ЦОС «Пифагор» появился ответ.",
        action_url="/feedback",
        action_label="Открыть обратную связь",
        extra_context={
            "answer_text": answer_text,
            "request_number": request_number,
        },
    )

    return send_templated_email(
        subject="Ответ на обращение в ЦОС «Пифагор»",
        to_email=to_email,
        template_base="emails/feedback/answered",
        context=context,
    )
