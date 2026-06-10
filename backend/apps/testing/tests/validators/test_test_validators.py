from __future__ import annotations

from apps.course.tests.factories import create_course, create_course_lesson
from apps.testing.tests.factories import create_test
from apps.testing.validators import (
    validate_test_attempt_settings,
    validate_test_scores,
    validate_test_structure,
)
from django.core.exceptions import ValidationError
from django.test import TestCase


class TestSettingsValidatorsTestCase(TestCase):
    """
    Тесты валидаторов настроек теста.
    """

    def test_validate_test_attempt_settings_allows_valid_attempts(self) -> None:
        """
        Валидатор пропускает корректное количество попыток.
        """

        exam = create_test(max_attempts=3)

        validate_test_attempt_settings(test=exam)

    def test_validate_test_attempt_settings_rejects_more_than_three(self) -> None:
        """
        Валидатор запрещает больше трёх попыток.
        """

        exam = create_test(max_attempts=4)

        with self.assertRaises(ValidationError):
            validate_test_attempt_settings(test=exam)

    def test_validate_test_scores_allows_valid_scores(self) -> None:
        """
        Валидатор пропускает корректные баллы.
        """

        exam = create_test(
            max_score=100,
            passing_score=50,
        )

        validate_test_scores(test=exam)

    def test_validate_test_scores_rejects_passing_above_max(self) -> None:
        """
        Валидатор запрещает проходной балл выше максимального.
        """

        exam = create_test(
            max_score=50,
            passing_score=80,
        )

        with self.assertRaises(ValidationError):
            validate_test_scores(test=exam)


class TestStructureValidatorsTestCase(TestCase):
    """
    Тесты валидаторов структуры теста.
    """

    def test_validate_test_structure_allows_matching_course_context(self) -> None:
        """
        Валидатор пропускает тест с контекстом выбранного курса.
        """

        course = create_course()
        exam = create_test(
            course=course,
            organization=course.organization,
            subject=course.subject,
        )

        validate_test_structure(test=exam)

    def test_validate_test_structure_rejects_foreign_lesson(self) -> None:
        """
        Валидатор запрещает урок из другого курса.
        """

        course = create_course()
        foreign_course = create_course()
        foreign_lesson = create_course_lesson(course=foreign_course)

        exam = create_test(
            course=course,
            lesson=foreign_lesson,
            organization=course.organization,
            subject=course.subject,
        )

        with self.assertRaises(ValidationError):
            validate_test_structure(test=exam)

    def test_validate_test_structure_rejects_foreign_organization(self) -> None:
        """
        Валидатор запрещает организацию, отличную от организации курса.
        """

        course = create_course()
        foreign_course = create_course()

        exam = create_test(
            course=course,
            organization=foreign_course.organization,
            subject=course.subject,
        )

        with self.assertRaises(ValidationError):
            validate_test_structure(test=exam)

    def test_validate_test_structure_rejects_foreign_subject(self) -> None:
        """
        Валидатор запрещает предмет, отличный от предмета курса.
        """

        course = create_course()
        foreign_course = create_course()

        exam = create_test(
            course=course,
            organization=course.organization,
            subject=foreign_course.subject,
        )

        with self.assertRaises(ValidationError):
            validate_test_structure(test=exam)
