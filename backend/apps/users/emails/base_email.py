from __future__ import annotations

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


def send_templated_email(
    *,
    subject: str,
    to_email: str,
    template_base: str,
    context: dict,
    from_email: str | None = None,
) -> int:
    """
    Отправляет email по HTML и TXT шаблонам.

    Для каждого письма ожидаются два шаблона:
        - <template_base>.txt
        - <template_base>.html

    Args:
        subject:
            Тема письма.
        to_email:
            Email получателя.
        template_base:
            Базовый путь к шаблону без расширения.
        context:
            Контекст шаблона.
        from_email:
            Email отправителя. Если не указан, используется DEFAULT_FROM_EMAIL.

    Returns:
        int: Количество успешно отправленных писем.
    """

    text_body = render_to_string(
        f"{template_base}.txt",
        context,
    )
    html_body = render_to_string(
        f"{template_base}.html",
        context,
    )

    message = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email or settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )
    message.attach_alternative(html_body, "text/html")

    return message.send()
