from __future__ import annotations

import pytest
from apps.users.tasks.email_tasks import (
    send_account_anonymized_task,
    send_account_blocked_task,
    send_account_scheduled_for_deletion_task,
    send_email_verification_task,
    send_guardian_link_approved_task,
    send_guardian_link_rejected_task,
    send_guardian_link_requested_task,
    send_guardian_registration_completed_task,
    send_join_request_approved_task,
    send_join_request_created_for_reviewer_task,
    send_join_request_rejected_task,
    send_learner_profile_required_task,
    send_teacher_registration_pending_task,
)
from apps.users.tests.factories import make_user
from django.core import mail


@pytest.fixture(autouse=True)
def clear_mail_outbox():
    """
    Очищает тестовый почтовый ящик перед каждым тестом.
    """

    mail.outbox = []


@pytest.mark.django_db
def test_send_email_verification_task() -> None:
    """
    Проверяет задачу отправки письма подтверждения email.
    """

    user = make_user(
        email="task-verify@example.com",
        is_email_verified=False,
    )

    result = send_email_verification_task(user_id=user.id)

    assert result is True
    assert len(mail.outbox) == 1
    assert user.email in mail.outbox[0].to


@pytest.mark.django_db
def test_send_email_verification_task_skips_verified_user() -> None:
    """
    Проверяет, что подтверждённому пользователю письмо не отправляется повторно.
    """

    user = make_user(
        email="task-verified@example.com",
        is_email_verified=True,
    )

    result = send_email_verification_task(user_id=user.id)

    assert result is True
    assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_send_email_verification_task_returns_false_for_missing_user() -> None:
    """
    Проверяет, что задача безопасно завершается, если пользователь не найден.
    """

    result = send_email_verification_task(user_id=999999)

    assert result is False
    assert len(mail.outbox) == 0


@pytest.mark.django_db
def test_send_teacher_registration_pending_task() -> None:
    """
    Проверяет задачу письма преподавателю о заявке.
    """

    user = make_user(email="task-teacher@example.com")

    result = send_teacher_registration_pending_task(user_id=user.id)

    assert result is True
    assert len(mail.outbox) == 1
    assert "Заявка преподавателя" in mail.outbox[0].subject


@pytest.mark.django_db
def test_send_learner_profile_required_task() -> None:
    """
    Проверяет задачу письма учащемуся о настройке профиля.
    """

    user = make_user(email="task-learner@example.com")

    result = send_learner_profile_required_task(user_id=user.id)

    assert result is True
    assert len(mail.outbox) == 1
    assert "Завершите настройку" in mail.outbox[0].subject


@pytest.mark.django_db
def test_send_guardian_registration_completed_task() -> None:
    """
    Проверяет задачу письма родителю после регистрации.
    """

    user = make_user(email="task-guardian@example.com")

    result = send_guardian_registration_completed_task(user_id=user.id)

    assert result is True
    assert len(mail.outbox) == 1
    assert user.email in mail.outbox[0].to


@pytest.mark.django_db
def test_send_join_request_approved_task() -> None:
    """
    Проверяет задачу письма о подтверждении заявки.
    """

    user = make_user(email="task-join-approved@example.com")

    result = send_join_request_approved_task(user_id=user.id)

    assert result is True
    assert len(mail.outbox) == 1
    assert "заявка" in mail.outbox[0].subject.lower()


@pytest.mark.django_db
def test_send_join_request_rejected_task() -> None:
    """
    Проверяет задачу письма об отклонении заявки.
    """

    user = make_user(email="task-join-rejected@example.com")

    result = send_join_request_rejected_task(
        user_id=user.id,
        review_comment="Данные требуют уточнения.",
    )

    assert result is True
    assert len(mail.outbox) == 1
    assert "Данные требуют уточнения." in mail.outbox[0].body


@pytest.mark.django_db
def test_send_join_request_created_for_reviewer_task() -> None:
    """
    Проверяет задачу письма проверяющему о новой заявке.
    """

    reviewer = make_user(email="task-reviewer@example.com")

    result = send_join_request_created_for_reviewer_task(
        reviewer_id=reviewer.id,
        applicant_name="Иван Иванов",
    )

    assert result is True
    assert len(mail.outbox) == 1
    assert reviewer.email in mail.outbox[0].to


@pytest.mark.django_db
def test_send_guardian_link_requested_task() -> None:
    """
    Проверяет задачу письма о запросе связи родителя и учащегося.
    """

    user = make_user(email="task-guardian-link-requested@example.com")

    result = send_guardian_link_requested_task(user_id=user.id)

    assert result is True
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_send_guardian_link_approved_task() -> None:
    """
    Проверяет задачу письма о подтверждении связи родителя и учащегося.
    """

    user = make_user(email="task-guardian-link-approved@example.com")

    result = send_guardian_link_approved_task(user_id=user.id)

    assert result is True
    assert len(mail.outbox) == 1


@pytest.mark.django_db
def test_send_guardian_link_rejected_task() -> None:
    """
    Проверяет задачу письма об отклонении связи родителя и учащегося.
    """

    user = make_user(email="task-guardian-link-rejected@example.com")

    result = send_guardian_link_rejected_task(
        user_id=user.id,
        review_comment="Связь не подтверждена.",
    )

    assert result is True
    assert len(mail.outbox) == 1
    assert "Связь не подтверждена." in mail.outbox[0].body


@pytest.mark.django_db
def test_send_account_blocked_task() -> None:
    """
    Проверяет задачу письма о блокировке аккаунта.
    """

    user = make_user(email="task-account-blocked@example.com")

    result = send_account_blocked_task(
        user_id=user.id,
        reason="Тестовая блокировка.",
    )

    assert result is True
    assert len(mail.outbox) == 1
    assert "Тестовая блокировка." in mail.outbox[0].body


@pytest.mark.django_db
def test_send_account_scheduled_for_deletion_task() -> None:
    """
    Проверяет задачу письма о запланированной анонимизации.
    """

    user = make_user(email="task-scheduled-delete@example.com")

    result = send_account_scheduled_for_deletion_task(
        user_id=user.id,
        scheduled_for_deletion_at="20 мая 2026, 12:00",
    )

    assert result is True
    assert len(mail.outbox) == 1
    assert "20 мая 2026, 12:00" in mail.outbox[0].body


@pytest.mark.django_db
def test_send_account_anonymized_task() -> None:
    """
    Проверяет задачу письма об анонимизации аккаунта.
    """

    user = make_user(email="task-account-anonymized@example.com")

    result = send_account_anonymized_task(user_id=user.id)

    assert result is True
    assert len(mail.outbox) == 1
