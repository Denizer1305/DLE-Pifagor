from __future__ import annotations

from datetime import timedelta

from apps.testing.services import build_attempt_integrity_report
from apps.testing.tests.factories import (
    create_answer,
    create_attempt,
    create_choice_question_with_options,
    create_test,
)
from django.test import TestCase
from django.utils import timezone


class TestIntegrityServicesTestCase(TestCase):
    """
    Тесты сервиса анализа добросовестности прохождения теста.
    """

    def test_integrity_report_returns_low_risk_for_regular_attempt(self) -> None:
        """
        Обычная попытка получает низкий уровень риска.
        """

        exam = create_test()
        attempt = create_attempt(
            test=exam,
            started_at=timezone.now() - timedelta(minutes=10),
            submitted_at=timezone.now(),
        )
        question = create_choice_question_with_options(test=exam)
        option = question.options.filter(is_correct=True).first()

        create_answer(
            attempt=attempt,
            question=question,
            selected_option=option,
        )

        report = build_attempt_integrity_report(attempt=attempt)

        self.assertEqual(report["risk_level"], "low")
        self.assertEqual(report["score"], 0)
        self.assertEqual(report["flags"], [])

    def test_integrity_report_detects_fast_completion(self) -> None:
        """
        Сервис фиксирует слишком быстрое прохождение.
        """

        exam = create_test()
        attempt = create_attempt(
            test=exam,
            started_at=timezone.now() - timedelta(seconds=5),
            submitted_at=timezone.now(),
        )
        question = create_choice_question_with_options(test=exam)
        option = question.options.filter(is_correct=True).first()

        create_answer(
            attempt=attempt,
            question=question,
            selected_option=option,
        )

        report = build_attempt_integrity_report(attempt=attempt)

        self.assertGreater(report["score"], 0)
        self.assertIn(
            "too_fast_completion",
            _extract_flag_codes(report=report),
        )

    def test_integrity_report_detects_identical_answer_pattern(self) -> None:
        """
        Сервис фиксирует совпадающий набор выбранных ответов.
        """

        exam = create_test()
        first_question = create_choice_question_with_options(test=exam)
        second_question = create_choice_question_with_options(test=exam)

        first_option = first_question.options.filter(is_correct=True).first()
        second_option = second_question.options.filter(is_correct=True).first()

        first_attempt = create_attempt(test=exam)
        second_attempt = create_attempt(test=exam)

        create_answer(
            attempt=first_attempt,
            question=first_question,
            selected_option=first_option,
        )
        create_answer(
            attempt=first_attempt,
            question=second_question,
            selected_option=second_option,
        )
        create_answer(
            attempt=second_attempt,
            question=first_question,
            selected_option=first_option,
        )
        create_answer(
            attempt=second_attempt,
            question=second_question,
            selected_option=second_option,
        )

        report = build_attempt_integrity_report(attempt=second_attempt)

        self.assertIn(
            "identical_answer_pattern",
            _extract_flag_codes(report=report),
        )

    def test_integrity_report_detects_similar_text_answers(self) -> None:
        """
        Сервис фиксирует похожие текстовые ответы.
        """

        exam = create_test()
        first_attempt = create_attempt(test=exam)
        second_attempt = create_attempt(test=exam)

        first_question = create_choice_question_with_options(test=exam)
        second_question = create_choice_question_with_options(test=exam)

        create_answer(
            attempt=first_attempt,
            question=first_question,
            text_answer="Пифагор — образовательная платформа.",
            selected_option=None,
        )
        create_answer(
            attempt=second_attempt,
            question=second_question,
            text_answer="Пифагор — образовательная платформа.",
            selected_option=None,
        )

        report = build_attempt_integrity_report(attempt=second_attempt)

        self.assertIn(
            "similar_text_answers",
            _extract_flag_codes(report=report),
        )


def _extract_flag_codes(*, report: dict) -> set[str]:
    """
    Возвращает коды признаков из integrity-отчёта.
    """

    return {flag["code"] for flag in report["flags"]}
