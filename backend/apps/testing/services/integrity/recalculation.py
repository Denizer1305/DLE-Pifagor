from __future__ import annotations

from difflib import SequenceMatcher

from apps.testing.constants import IntegrityRiskLevel


def build_attempt_integrity_report_payload(*, attempt) -> dict:
    """
    Формирует payload отчёта добросовестности прохождения теста.

    Отчёт не доказывает списывание, а только показывает признаки риска.
    """

    flags = []

    flags.extend(_detect_fast_completion(attempt=attempt))
    flags.extend(_detect_identical_answer_pattern(attempt=attempt))
    flags.extend(_detect_similar_text_answers(attempt=attempt))

    score = _calculate_integrity_score(flags=flags)
    risk_level = calculate_integrity_risk_level(score=score)

    return {
        "score": score,
        "risk_level": risk_level,
        "flags_data": flags,
    }


def calculate_integrity_risk_level(*, score: int) -> str:
    """
    Рассчитывает уровень риска по итоговому баллу.
    """

    if score >= 70:
        return IntegrityRiskLevel.HIGH

    if score >= 35:
        return IntegrityRiskLevel.MEDIUM

    return IntegrityRiskLevel.LOW


def _detect_fast_completion(*, attempt) -> list[dict]:
    """
    Проверяет слишком быстрое прохождение теста.
    """

    if not attempt.started_at or not attempt.submitted_at:
        return []

    duration_seconds = (attempt.submitted_at - attempt.started_at).total_seconds()

    answers_count = attempt.answers.count()

    if answers_count == 0:
        return []

    if duration_seconds > 20:
        return []

    return [
        {
            "code": "too_fast_completion",
            "title": "Слишком быстрое прохождение",
            "description": (
                "Попытка была отправлена слишком быстро относительно "
                "количества ответов."
            ),
            "weight": 25,
            "meta": {
                "duration_seconds": int(duration_seconds),
                "answers_count": answers_count,
            },
        }
    ]


def _detect_identical_answer_pattern(*, attempt) -> list[dict]:
    """
    Проверяет совпадение набора выбранных вариантов с другой попыткой.
    """

    current_pattern = _build_choice_answer_pattern(attempt=attempt)

    if not current_pattern:
        return []

    previous_attempts = (
        attempt.__class__.objects.filter(test=attempt.test)
        .exclude(id=attempt.id)
        .prefetch_related("answers")
    )

    for previous_attempt in previous_attempts:
        previous_pattern = _build_choice_answer_pattern(
            attempt=previous_attempt,
        )

        if previous_pattern and previous_pattern == current_pattern:
            return [
                {
                    "code": "identical_answer_pattern",
                    "title": "Совпадающий набор ответов",
                    "description": (
                        "Набор выбранных вариантов совпадает с другой "
                        "попыткой по этому тесту."
                    ),
                    "weight": 35,
                    "meta": {
                        "matched_attempt_id": previous_attempt.id,
                    },
                }
            ]

    return []


def _detect_similar_text_answers(*, attempt) -> list[dict]:
    """
    Проверяет совпадение текстовых ответов с другой попыткой.
    """

    current_text = _build_text_answer_pattern(attempt=attempt)

    if not current_text:
        return []

    previous_attempts = (
        attempt.__class__.objects.filter(test=attempt.test)
        .exclude(id=attempt.id)
        .prefetch_related("answers")
    )

    for previous_attempt in previous_attempts:
        previous_text = _build_text_answer_pattern(attempt=previous_attempt)

        if not previous_text:
            continue

        similarity = SequenceMatcher(
            None,
            current_text,
            previous_text,
        ).ratio()

        if similarity >= 0.9:
            return [
                {
                    "code": "similar_text_answers",
                    "title": "Похожие текстовые ответы",
                    "description": (
                        "Текстовые ответы сильно похожи на ответы " "из другой попытки."
                    ),
                    "weight": 35,
                    "meta": {
                        "matched_attempt_id": previous_attempt.id,
                        "similarity": round(similarity, 2),
                    },
                }
            ]

    return []


def _calculate_integrity_score(*, flags: list[dict]) -> int:
    """
    Рассчитывает итоговый риск по признакам.
    """

    score = sum(int(flag.get("weight", 0)) for flag in flags)

    return min(score, 100)


def _build_choice_answer_pattern(*, attempt) -> tuple:
    """
    Формирует паттерн выбранных вариантов ответа.
    """

    pattern = []

    for answer in attempt.answers.order_by("question_id"):
        if answer.selected_option_id:
            pattern.append(
                (
                    answer.question_id,
                    answer.selected_option_id,
                )
            )
            continue

        if answer.selected_options_data:
            pattern.append(
                (
                    answer.question_id,
                    tuple(sorted(answer.selected_options_data)),
                )
            )

    return tuple(pattern)


def _build_text_answer_pattern(*, attempt) -> str:
    """
    Формирует паттерн текстовых ответов.
    """

    text_answers = []

    for answer in attempt.answers.order_by("question_id"):
        text_answer = answer.text_answer.strip()

        if text_answer:
            text_answers.append(text_answer.lower())

    return " ".join(text_answers)
