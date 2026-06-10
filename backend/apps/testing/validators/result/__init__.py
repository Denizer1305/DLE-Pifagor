from __future__ import annotations

from .aggregation import validate_result_attempt_counters, validate_result_scores
from .visibility import validate_result_blocking, validate_result_visibility


def validate_result(*, result) -> None:
    """
    Запускает полную валидацию итогового результата.
    """

    validate_result_attempt_counters(result=result)
    validate_result_scores(result=result)
    validate_result_visibility(result=result)
    validate_result_blocking(result=result)


__all__ = [
    "validate_result",
    "validate_result_attempt_counters",
    "validate_result_blocking",
    "validate_result_scores",
    "validate_result_visibility",
]
