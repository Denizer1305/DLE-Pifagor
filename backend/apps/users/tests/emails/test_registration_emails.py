from __future__ import annotations

import pytest
from apps.users.emails.registration_emails import (
    send_email_verification_email,
    send_guardian_registration_completed_email,
    send_learner_profile_required_email,
    send_teacher_registration_pending_email,
)
from apps.users.tests.emails.assertions import assert_email_was_sent, get_sent_message
from apps.users.tests.factories import make_user


@pytest.mark.django_db
def test_send_email_verification_email() -> None:
    """
    Проверяет отправку письма подтверждения email.
    """

    user = make_user(
        email="verify-email@example.com",
        first_name="Иван",
        middle_name="Иванович",
        is_email_verified=False,
    )

    result = send_email_verification_email(user=user)

    assert result == 1
    assert_email_was_sent(
        expected_subject_part="Подтверждение email",
        expected_to=user.email,
    )

    message = get_sent_message()

    assert "http://testserver" in message.body
    assert "Перейдите по ссылке подтверждения" in message.body


@pytest.mark.django_db
def test_send_teacher_registration_pending_email() -> None:
    """
    Проверяет отправку письма преподавателю о заявке на проверку.
    """

    user = make_user(
        email="teacher@example.com",
        first_name="Елена",
        middle_name="Александровна",
    )

    result = send_teacher_registration_pending_email(user=user)

    assert result == 1
    assert_email_was_sent(
        expected_subject_part="Заявка преподавателя",
        expected_to=user.email,
    )

    message = get_sent_message()

    assert "администратору образовательной организации" in message.body


@pytest.mark.django_db
def test_send_learner_profile_required_email() -> None:
    """
    Проверяет отправку письма учащемуся о заполнении профиля.
    """

    user = make_user(
        email="learner-email@example.com",
        first_name="Денис",
    )

    result = send_learner_profile_required_email(user=user)

    assert result == 1
    assert_email_was_sent(
        expected_subject_part="Завершите настройку",
        expected_to=user.email,
    )

    message = get_sent_message()

    assert "настройку профиля учащегося" in message.body


@pytest.mark.django_db
def test_send_guardian_registration_completed_email() -> None:
    """
    Проверяет отправку письма родителю после регистрации.
    """

    user = make_user(
        email="guardian-email@example.com",
        first_name="Мария",
        middle_name="Петровна",
    )

    result = send_guardian_registration_completed_email(user=user)

    assert result == 1
    assert_email_was_sent(
        expected_subject_part="Регистрация родителя",
        expected_to=user.email,
    )

    message = get_sent_message()

    assert "кабинет родителя" in message.body.lower()
