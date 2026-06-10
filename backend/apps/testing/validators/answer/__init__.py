from __future__ import annotations

from .checking import validate_answer_relations, validate_answer_scores
from .payload import validate_answer_payload


def validate_answer(*, answer) -> None:
    """
    Запускает полную валидацию ответа.
    """

    validate_answer_relations(answer=answer)
    validate_answer_payload(answer=answer)
    validate_answer_scores(answer=answer)


__all__ = [
    "validate_answer",
    "validate_answer_payload",
    "validate_answer_relations",
    "validate_answer_scores",
]
