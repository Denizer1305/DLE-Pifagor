from __future__ import annotations

from apps.testing.constants import TestAttemptStatus, TestStatus
from apps.testing.services.taking import (
    build_taking_test_payload,
    ensure_learner_can_continue_attempt,
    ensure_learner_can_take_test,
    validate_attempt_available_for_taking,
    validate_attempt_belongs_to_learner,
    validate_learner_has_test_access,
    validate_test_available_for_taking,
)
from apps.testing.tests.factories import (
    create_attempt,
    create_choice_question_with_options,
    create_course,
    create_course_enrollment,
    create_learner,
    create_test,
)
from django.core.exceptions import ValidationError
from django.test import TestCase


class TakingAccessServicesTestCase(TestCase):
    """
    Тесты доступа обучающегося к прохождению теста.
    """

    def test_validate_test_available_for_taking_allows_published_test(self) -> None:
        """
        Опубликованный активный тест доступен для прохождения.
        """

        exam = create_test(
            status=TestStatus.PUBLISHED,
            is_active=True,
        )

        validate_test_available_for_taking(test=exam)

    def test_validate_test_available_for_taking_rejects_draft_test(self) -> None:
        """
        Черновой тест недоступен для прохождения.
        """

        exam = create_test(status=TestStatus.DRAFT)

        with self.assertRaises(ValidationError):
            validate_test_available_for_taking(test=exam)

    def test_validate_learner_has_test_access_allows_enrolled_learner(self) -> None:
        """
        Обучающийся с записью на курс имеет доступ к тесту.
        """

        learner = create_learner()
        course = create_course()
        exam = create_test(course=course)
        create_course_enrollment(
            course=course,
            learner=learner,
        )

        validate_learner_has_test_access(
            test=exam,
            learner=learner,
        )

    def test_validate_learner_has_test_access_rejects_foreign_learner(self) -> None:
        """
        Обучающийся без записи на курс не имеет доступа к тесту.
        """

        learner = create_learner()
        course = create_course()
        exam = create_test(course=course)

        with self.assertRaises(ValidationError):
            validate_learner_has_test_access(
                test=exam,
                learner=learner,
            )

    def test_validate_attempt_belongs_to_learner_allows_owner(self) -> None:
        """
        Попытка доступна своему обучающемуся.
        """

        attempt = create_attempt()

        validate_attempt_belongs_to_learner(
            attempt=attempt,
            learner=attempt.learner,
        )

    def test_validate_attempt_belongs_to_learner_rejects_foreign_learner(
        self,
    ) -> None:
        """
        Попытка недоступна другому обучающемуся.
        """

        attempt = create_attempt()
        foreign_learner = create_learner()

        with self.assertRaises(ValidationError):
            validate_attempt_belongs_to_learner(
                attempt=attempt,
                learner=foreign_learner,
            )

    def test_validate_attempt_available_for_taking_allows_started_attempt(
        self,
    ) -> None:
        """
        Начатую попытку можно продолжать.
        """

        attempt = create_attempt(status=TestAttemptStatus.STARTED)

        validate_attempt_available_for_taking(attempt=attempt)

    def test_validate_attempt_available_for_taking_rejects_submitted_attempt(
        self,
    ) -> None:
        """
        Отправленную попытку нельзя продолжать.
        """

        attempt = create_attempt(status=TestAttemptStatus.SUBMITTED)

        with self.assertRaises(ValidationError):
            validate_attempt_available_for_taking(attempt=attempt)

    def test_ensure_learner_can_take_test_allows_valid_context(self) -> None:
        """
        Полная проверка доступа пропускает валидный контекст.
        """

        learner = create_learner()
        course = create_course()
        exam = create_test(
            course=course,
            status=TestStatus.PUBLISHED,
            is_active=True,
        )
        create_course_enrollment(
            course=course,
            learner=learner,
        )

        ensure_learner_can_take_test(
            test=exam,
            learner=learner,
        )

    def test_ensure_learner_can_continue_attempt_allows_owner_started_attempt(
        self,
    ) -> None:
        """
        Обучающийся может продолжить свою начатую попытку.
        """

        attempt = create_attempt(status=TestAttemptStatus.STARTED)

        ensure_learner_can_continue_attempt(
            attempt=attempt,
            learner=attempt.learner,
        )


class TakingPayloadServicesTestCase(TestCase):
    """
    Тесты безопасного payload прохождения теста.
    """

    def test_build_taking_test_payload_returns_test_attempt_questions(self) -> None:
        """
        Payload прохождения содержит тест, попытку и вопросы.
        """

        exam = create_test(
            status=TestStatus.PUBLISHED,
            is_active=True,
        )
        attempt = create_attempt(
            test=exam,
            status=TestAttemptStatus.STARTED,
        )
        create_choice_question_with_options(test=exam)

        payload = build_taking_test_payload(
            test=exam,
            attempt=attempt,
        )

        self.assertIn("test", payload)
        self.assertIn("attempt", payload)
        self.assertIn("questions", payload)
        self.assertEqual(payload["test"]["id"], exam.id)
        self.assertEqual(payload["attempt"]["id"], attempt.id)
        self.assertEqual(len(payload["questions"]), 1)

    def test_build_taking_test_payload_does_not_leak_correct_answers(self) -> None:
        """
        Payload прохождения не отдаёт правильные ответы и feedback.
        """

        exam = create_test(
            status=TestStatus.PUBLISHED,
            is_active=True,
        )
        attempt = create_attempt(
            test=exam,
            status=TestAttemptStatus.STARTED,
        )
        create_choice_question_with_options(test=exam)

        payload = build_taking_test_payload(
            test=exam,
            attempt=attempt,
        )

        question_payload = payload["questions"][0]
        option_payload = question_payload["options"][0]

        self.assertNotIn("expected_text_answer", question_payload)
        self.assertNotIn("expected_number_answer", question_payload)
        self.assertNotIn("source_bank_item", question_payload)
        self.assertNotIn("is_correct", option_payload)
        self.assertNotIn("score", option_payload)
        self.assertNotIn("feedback", option_payload)
