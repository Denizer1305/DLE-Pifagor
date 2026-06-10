from __future__ import annotations

from difflib import SequenceMatcher

from apps.testing.models import TestAttempt
from apps.testing.services.integrity.payloads import IntegrityFlag, IntegrityReport

MIN_SECONDS_PER_QUESTION = 20
HIGH_SIMILARITY_RATIO = 0.9


def build_attempt_integrity_report(
    *,
    attempt: TestAttempt,
) -> dict:
    """
    Формирует отчёт о возможных признаках списывания.

    Отчёт не является доказательством списывания.
    Он только помогает преподавателю обратить внимание на попытку.
    """

    report = IntegrityReport()

    _check_fast_completion(
        attempt=attempt,
        report=report,
    )
    _check_identical_answer_pattern(
        attempt=attempt,
        report=report,
    )
    _check_text_answer_similarity(
        attempt=attempt,
        report=report,
    )

    report.calculate_risk_level()

    return report.as_dict()


def _check_fast_completion(
    *,
    attempt: TestAttempt,
    report: IntegrityReport,
) -> None:
    """
    Проверяет подозрительно быстрое прохождение теста.
    """

    if not attempt.started_at or not attempt.submitted_at:
        return

    answers_count = attempt.answers.count()

    if answers_count == 0:
        return

    duration_seconds = (attempt.submitted_at - attempt.started_at).total_seconds()

    min_expected_seconds = answers_count * MIN_SECONDS_PER_QUESTION

    if duration_seconds >= min_expected_seconds:
        return

    report.add_flag(
        IntegrityFlag(
            code="too_fast_completion",
            title="Слишком быстрое прохождение",
            description=("Тест был выполнен быстрее минимального ожидаемого времени."),
            weight=30,
        )
    )


def _check_identical_answer_pattern(
    *,
    attempt: TestAttempt,
    report: IntegrityReport,
) -> None:
    """
    Проверяет совпадение набора ответов с другими попытками.
    """

    current_pattern = _build_answer_pattern(attempt=attempt)

    if not current_pattern:
        return

    other_attempts = (
        TestAttempt.objects.filter(test_id=attempt.test_id)
        .exclude(id=attempt.id)
        .prefetch_related("answers")
    )

    for other_attempt in other_attempts:
        other_pattern = _build_answer_pattern(attempt=other_attempt)

        if current_pattern != other_pattern:
            continue

        report.add_flag(
            IntegrityFlag(
                code="identical_answer_pattern",
                title="Совпадающий набор ответов",
                description=(
                    "Набор выбранных ответов полностью совпадает "
                    "с другой попыткой по этому тесту."
                ),
                weight=35,
            )
        )
        return


def _check_text_answer_similarity(
    *,
    attempt: TestAttempt,
    report: IntegrityReport,
) -> None:
    """
    Проверяет похожесть текстовых ответов с другими попытками.
    """

    current_text = _build_text_answers_snapshot(attempt=attempt)

    if not current_text:
        return

    other_attempts = (
        TestAttempt.objects.filter(test_id=attempt.test_id)
        .exclude(id=attempt.id)
        .prefetch_related("answers")
    )

    for other_attempt in other_attempts:
        other_text = _build_text_answers_snapshot(attempt=other_attempt)

        if not other_text:
            continue

        similarity = SequenceMatcher(
            None,
            current_text,
            other_text,
        ).ratio()

        if similarity < HIGH_SIMILARITY_RATIO:
            continue

        report.add_flag(
            IntegrityFlag(
                code="similar_text_answers",
                title="Похожие текстовые ответы",
                description=(
                    "Текстовые ответы сильно похожи на ответы "
                    "другой попытки по этому тесту."
                ),
                weight=35,
            )
        )
        return


def _build_answer_pattern(*, attempt: TestAttempt) -> tuple:
    """
    Собирает технический слепок выбранных ответов.
    """

    pattern = []

    for answer in attempt.answers.all().order_by("question_id"):
        pattern.append(
            (
                answer.question_id,
                answer.selected_option_id,
                tuple(answer.selected_options_data or []),
                str(answer.number_answer or ""),
            )
        )

    return tuple(pattern)


def _build_text_answers_snapshot(*, attempt: TestAttempt) -> str:
    """
    Собирает текстовые ответы попытки в одну строку.
    """

    parts = []

    for answer in attempt.answers.all().order_by("question_id"):
        text = answer.text_answer.strip().lower()

        if text:
            parts.append(text)

    return "\n".join(parts)
