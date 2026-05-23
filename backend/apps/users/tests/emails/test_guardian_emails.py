from __future__ import annotations

import pytest
from apps.users.emails.guardian_emails import (
    send_guardian_link_approved_email,
    send_guardian_link_rejected_email,
    send_guardian_link_requested_email,
)
from apps.users.tests.emails.assertions import assert_email_was_sent, get_sent_message
from apps.users.tests.factories import make_user


@pytest.mark.django_db
def test_send_guardian_link_requested_email() -> None:
    """
    Проверяет отправку письма о запросе связи родителя и учащегося.
    """

    user = make_user(email="guardian-link-requested@example.com")

    result = send_guardian_link_requested_email(user=user)

    assert result == 1
    assert_email_was_sent(
        expected_subject_part="Запрос на связь",
        expected_to=user.email,
    )

    message = get_sent_message()

    assert "связь родителя и учащегося" in message.body


@pytest.mark.django_db
def test_send_guardian_link_approved_email() -> None:
    """
    Проверяет отправку письма о подтверждении связи родителя и учащегося.
    """

    user = make_user(email="guardian-link-approved@example.com")

    result = send_guardian_link_approved_email(user=user)

    assert result == 1
    assert_email_was_sent(
        expected_subject_part="Связь родителя",
        expected_to=user.email,
    )

    message = get_sent_message()

    assert "Связь родителя и учащегося подтверждена" in message.body


@pytest.mark.django_db
def test_send_guardian_link_rejected_email_with_comment() -> None:
    """
    Проверяет отправку письма об отклонении связи родителя и учащегося.
    """

    user = make_user(email="guardian-link-rejected@example.com")

    result = send_guardian_link_rejected_email(
        user=user,
        review_comment="Не совпадают данные учащегося.",
    )

    assert result == 1
    assert_email_was_sent(
        expected_subject_part="не подтверждена",
        expected_to=user.email,
    )

    message = get_sent_message()

    assert "Не совпадают данные учащегося." in message.body
