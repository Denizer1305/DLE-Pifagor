from __future__ import annotations

from .option_rules import validate_question_options_for_publish
from .score_rules import validate_question_score
from .type_rules import validate_question_expected_answers, validate_question_type_rules


def validate_question(*, question) -> None:
    """
    Запускает базовую валидацию вопроса.
    """

    validate_question_type_rules(question=question)
    validate_question_expected_answers(question=question)
    validate_question_score(question=question)


__all__ = [
    "validate_question",
    "validate_question_expected_answers",
    "validate_question_options_for_publish",
    "validate_question_score",
    "validate_question_type_rules",
]
