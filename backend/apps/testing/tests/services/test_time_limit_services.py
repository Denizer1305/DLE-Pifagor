from __future__ import annotations

from datetime import timedelta

from apps.testing.constants import TestAttemptStatus
from apps.testing.services.attempt.time_limit import (
    calculate_attempt_expires_at,
    ensure_attempt_accepts_answers_by_time,
    ensure_attempt_can_be_submitted_by_time,
    expire_attempt_if_needed,
    set_attempt_expires_at,
)
from apps.testing.tests.factories import create_attempt, create_test
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone


class AttemptTimeLimitServicesTestCase(TestCase):
    """
    Тесты сервисов ограничения времени попытки.
    """

    def test_calculate_attempt_expires_at_returns_none_without_limit(self) -> None:
        """
        Без лимита времени expires_at не рассчитывается.
        """

        exam = create_test(time_limit_minutes=None)
        attempt = create_attempt(test=exam)

        self.assertIsNone(calculate_attempt_expires_at(attempt=attempt))

    def test_calculate_attempt_expires_at_returns_datetime_with_limit(self) -> None:
        """
        При наличии лимита рассчитывается время истечения.
        """

        exam = create_test(time_limit_minutes=30)
        started_at = timezone.now()
        attempt = create_attempt(
            test=exam,
            started_at=started_at,
        )

        expires_at = calculate_attempt_expires_at(attempt=attempt)

        self.assertEqual(
            expires_at,
            started_at + timedelta(minutes=30),
        )

    def test_set_attempt_expires_at_saves_value(self) -> None:
        """
        Сервис сохраняет время истечения попытки.
        """

        exam = create_test(time_limit_minutes=20)
        attempt = create_attempt(
            test=exam,
            started_at=timezone.now(),
            expires_at=None,
        )

        set_attempt_expires_at(attempt=attempt)

        attempt.refresh_from_db()

        self.assertIsNotNone(attempt.expires_at)

    def test_expire_attempt_if_needed_marks_attempt_expired(self) -> None:
        """
        Сервис помечает начатую просроченную попытку истёкшей.
        """

        attempt = create_attempt(
            status=TestAttemptStatus.STARTED,
            expires_at=timezone.now() - timedelta(minutes=1),
        )

        expired_attempt = expire_attempt_if_needed(attempt=attempt)

        self.assertEqual(expired_attempt.status, TestAttemptStatus.EXPIRED)
        self.assertIsNotNone(expired_attempt.expired_at)

    def test_expire_attempt_if_needed_does_not_touch_submitted_attempt(self) -> None:
        """
        Сервис не меняет статус уже отправленной попытки.
        """

        attempt = create_attempt(
            status=TestAttemptStatus.SUBMITTED,
            expires_at=timezone.now() - timedelta(minutes=1),
        )

        updated_attempt = expire_attempt_if_needed(attempt=attempt)

        self.assertEqual(updated_attempt.status, TestAttemptStatus.SUBMITTED)

    def test_ensure_attempt_accepts_answers_allows_active_attempt(self) -> None:
        """
        Попытка до истечения времени принимает ответы.
        """

        attempt = create_attempt(
            status=TestAttemptStatus.STARTED,
            expires_at=timezone.now() + timedelta(minutes=10),
        )

        ensure_attempt_accepts_answers_by_time(attempt=attempt)

    def test_ensure_attempt_accepts_answers_rejects_expired_attempt(self) -> None:
        """
        Просроченная попытка не принимает ответы.
        """

        attempt = create_attempt(
            status=TestAttemptStatus.STARTED,
            expires_at=timezone.now() - timedelta(minutes=1),
        )

        with self.assertRaises(ValidationError):
            ensure_attempt_accepts_answers_by_time(attempt=attempt)

    def test_ensure_attempt_can_be_submitted_allows_active_attempt(self) -> None:
        """
        Попытку можно отправить до истечения времени.
        """

        attempt = create_attempt(
            status=TestAttemptStatus.STARTED,
            expires_at=timezone.now() + timedelta(minutes=10),
        )

        ensure_attempt_can_be_submitted_by_time(attempt=attempt)

    def test_ensure_attempt_can_be_submitted_rejects_expired_attempt(self) -> None:
        """
        Просроченную попытку нельзя отправить.
        """

        attempt = create_attempt(
            status=TestAttemptStatus.STARTED,
            expires_at=timezone.now() - timedelta(minutes=1),
        )

        with self.assertRaises(ValidationError):
            ensure_attempt_can_be_submitted_by_time(attempt=attempt)
