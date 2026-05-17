from __future__ import annotations

import pytest
from apps.users.emails.lifecycle_emails import (
    send_account_anonymized_email,
    send_account_blocked_email,
    send_account_scheduled_for_deletion_email,
)
from apps.users.tests.emails.assertions import assert_email_was_sent, get_sent_message
from apps.users.tests.factories import make_user


@pytest.mark.django_db
def test_send_account_blocked_email_with_reason() -> None:
    """
    Проверяет отправку письма о блокировке аккаунта.
    """

    user = make_user(email="blocked-email@example.com")

    result = send_account_blocked_email(
        user=user,
        reason="Аккаунт временно ограничен администратором.",
    )

    assert result == 1
    assert_email_was_sent(
        expected_subject_part="заблокирован",
        expected_to=user.email,
    )

    message = get_sent_message()

    assert "Аккаунт временно ограничен администратором." in message.body


@pytest.mark.django_db
def test_send_account_scheduled_for_deletion_email() -> None:
    """
    Проверяет отправку письма о запланированной анонимизации.
    """

    user = make_user(email="scheduled-delete@example.com")

    result = send_account_scheduled_for_deletion_email(
        user=user,
        scheduled_for_deletion_at="20 мая 2026, 12:00",
    )

    assert result == 1
    assert_email_was_sent(
        expected_subject_part="анонимизирован",
        expected_to=user.email,
    )

    message = get_sent_message()

    assert "20 мая 2026, 12:00" in message.body


@pytest.mark.django_db
def test_send_account_anonymized_email() -> None:
    """
    Проверяет отправку письма об анонимизации аккаунта.
    """

    user = make_user(email="anonymized-email@example.com")

    result = send_account_anonymized_email(user=user)

    assert result == 1
    assert_email_was_sent(
        expected_subject_part="анонимизирован",
        expected_to=user.email,
    )

    message = get_sent_message()

    assert "Персональные данные обезличены" in message.body
