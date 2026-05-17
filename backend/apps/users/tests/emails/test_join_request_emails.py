from __future__ import annotations

import pytest
from apps.users.emails.join_request_emails import (
    send_join_request_approved_email,
    send_join_request_created_for_reviewer_email,
    send_join_request_rejected_email,
)
from apps.users.tests.emails.assertions import assert_email_was_sent, get_sent_message
from apps.users.tests.factories import make_user


@pytest.mark.django_db
def test_send_join_request_approved_email() -> None:
    """
    Проверяет отправку письма о подтверждении заявки.
    """

    user = make_user(email="approved@example.com")

    result = send_join_request_approved_email(user=user)

    assert result == 1
    assert_email_was_sent(
        expected_subject_part="заявка",
        expected_to=user.email,
    )

    message = get_sent_message()

    assert "Ваша заявка подтверждена" in message.body


@pytest.mark.django_db
def test_send_join_request_rejected_email_with_comment() -> None:
    """
    Проверяет отправку письма об отклонении заявки с комментарием.
    """

    user = make_user(email="rejected@example.com")

    result = send_join_request_rejected_email(
        user=user,
        review_comment="Проверьте выбранную образовательную организацию.",
    )

    assert result == 1
    assert_email_was_sent(
        expected_subject_part="отклонена",
        expected_to=user.email,
    )

    message = get_sent_message()

    assert "Проверьте выбранную образовательную организацию." in message.body


@pytest.mark.django_db
def test_send_join_request_created_for_reviewer_email() -> None:
    """
    Проверяет отправку письма проверяющему о новой заявке.
    """

    reviewer = make_user(
        email="reviewer@example.com",
        first_name="Ольга",
        middle_name="Сергеевна",
    )

    result = send_join_request_created_for_reviewer_email(
        reviewer=reviewer,
        applicant_name="Иван Иванов",
    )

    assert result == 1
    assert_email_was_sent(
        expected_subject_part="Новая заявка",
        expected_to=reviewer.email,
    )

    message = get_sent_message()

    assert "Иван Иванов" in message.body
