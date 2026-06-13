from __future__ import annotations

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.testing.constants import TestAttemptStatus
from apps.testing.tests.factories import create_attempt
from apps.testing.validators import (
    validate_attempt_can_accept_answers_by_time,
    validate_attempt_can_be_submitted_by_time,
    validate_attempt_time_limit,
)


class AttemptTimeLimitValidatorsTestCase(TestCase):
    """
    Тесты валидаторов ограничения времени попытки.
    """

    def test_attempt_without_expires_at_is_allowed(self) -> None:
        """
        Попытка без ограничения времени проходит проверку.
        """

        attempt = create_attempt(expires_at=None)

        validate_attempt_time_limit(attempt=attempt)

    def test_attempt_with_future_expires_at_is_allowed(self) -> None:
        """
        Попытка с будущим временем истечения проходит проверку.
        """

        attempt = create_attempt(
            expires_at=timezone.now() + timedelta(minutes=10),
        )

        validate_attempt_time_limit(attempt=attempt)

    def test_attempt_with_expired_status_is_rejected(self) -> None:
        """
        Попытка со статусом expired не проходит проверку.
        """

        attempt = create_attempt(
            status=TestAttemptStatus.EXPIRED,
            expires_at=timezone.now() + timedelta(minutes=10),
        )

        with self.assertRaises(ValidationError):
            validate_attempt_time_limit(attempt=attempt)

    def test_attempt_with_past_expires_at_is_rejected(self) -> None:
        """
        Попытка с прошедшим временем истечения не проходит проверку.
        """

        attempt = create_attempt(
            expires_at=timezone.now() - timedelta(minutes=1),
        )

        with self.assertRaises(ValidationError):
            validate_attempt_time_limit(attempt=attempt)

    def test_attempt_can_accept_answers_by_time(self) -> None:
        """
        Попытка может принимать ответы до истечения времени.
        """

        attempt = create_attempt(
            expires_at=timezone.now() + timedelta(minutes=10),
        )

        validate_attempt_can_accept_answers_by_time(attempt=attempt)

    def test_attempt_cannot_accept_answers_after_time_expired(self) -> None:
        """
        Попытка не принимает ответы после истечения времени.
        """

        attempt = create_attempt(
            expires_at=timezone.now() - timedelta(minutes=1),
        )

        with self.assertRaises(ValidationError):
            validate_attempt_can_accept_answers_by_time(attempt=attempt)

    def test_attempt_can_be_submitted_by_time(self) -> None:
        """
        Попытку можно отправить до истечения времени.
        """

        attempt = create_attempt(
            expires_at=timezone.now() + timedelta(minutes=10),
        )

        validate_attempt_can_be_submitted_by_time(attempt=attempt)

    def test_attempt_cannot_be_submitted_after_time_expired(self) -> None:
        """
        Попытку нельзя отправить после истечения времени.
        """

        attempt = create_attempt(
            expires_at=timezone.now() - timedelta(minutes=1),
        )

        with self.assertRaises(ValidationError):
            validate_attempt_can_be_submitted_by_time(attempt=attempt)