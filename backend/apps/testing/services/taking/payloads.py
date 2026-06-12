from __future__ import annotations

from apps.testing.selectors import (
    taking_options_for_test_queryset,
    taking_question_list_queryset,
)


def build_taking_test_payload(
    *,
    test,
    attempt,
) -> dict:
    """
    Собирает безопасный payload прохождения теста.

    Payload не содержит правильные ответы, expected answers,
    is_correct, score вариантов и feedback.
    """

    questions = taking_question_list_queryset(test_id=test.id)
    options_by_question_id = _group_options_by_question_id(test_id=test.id)

    return {
        "test": {
            "id": test.id,
            "title": test.title,
            "description": test.description,
            "instructions": test.instructions,
            "time_limit_minutes": test.time_limit_minutes,
            "shuffle_questions": test.shuffle_questions,
            "shuffle_options": test.shuffle_options,
        },
        "attempt": {
            "id": attempt.id,
            "attempt_number": attempt.attempt_number,
            "status": attempt.status,
            "started_at": attempt.started_at,
            "expires_at": attempt.expires_at,
        },
        "questions": [
            _build_taking_question_payload(
                question=question,
                options=options_by_question_id.get(question.id, []),
            )
            for question in questions
        ],
    }


def _group_options_by_question_id(*, test_id: int) -> dict[int, list]:
    """
    Группирует варианты ответа по вопросам теста.
    """

    grouped_options: dict[int, list] = {}

    for option in taking_options_for_test_queryset(test_id=test_id):
        grouped_options.setdefault(option.question_id, []).append(option)

    return grouped_options


def _build_taking_question_payload(
    *,
    question,
    options: list,
) -> dict:
    """
    Собирает безопасный payload вопроса для прохождения.
    """

    return {
        "id": question.id,
        "question_type": question.question_type,
        "check_mode": question.check_mode,
        "title": question.title,
        "text": question.text,
        "order": question.order,
        "score": question.score,
        "is_required": question.is_required,
        "options": [_build_taking_option_payload(option=option) for option in options],
    }


def _build_taking_option_payload(*, option) -> dict:
    """
    Собирает безопасный payload варианта ответа.
    """

    return {
        "id": option.id,
        "text": option.text,
        "order": option.order,
    }
