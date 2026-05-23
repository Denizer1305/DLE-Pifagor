from __future__ import annotations

from django.core import mail


def assert_email_was_sent(*, expected_subject_part: str, expected_to: str) -> None:
    """
    Проверяет, что письмо было отправлено в тестовый почтовый ящик.

    Args:
        expected_subject_part:
            Ожидаемая часть темы письма.
        expected_to:
            Email получателя.
    """

    assert len(mail.outbox) == 1

    message = mail.outbox[0]

    assert expected_subject_part in message.subject
    assert expected_to in message.to
    assert message.body
    assert "С уважением, команда ЦОС «Пифагор»" in message.body

    assert message.alternatives
    assert message.alternatives[0][1] == "text/html"
    assert "Цифровая образовательная среда «Пифагор»" in message.alternatives[0][0]


def get_sent_message():
    """
    Возвращает единственное отправленное письмо.

    Returns:
        EmailMultiAlternatives: Отправленное письмо.
    """

    assert len(mail.outbox) == 1

    return mail.outbox[0]
