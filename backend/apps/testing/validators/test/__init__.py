from __future__ import annotations

from .attempts import validate_test_attempt_settings
from .scores import validate_test_scores
from .structure import validate_test_structure


def validate_test(*, test) -> None:
    """
    Запускает полную валидацию теста.
    """

    validate_test_attempt_settings(test=test)
    validate_test_scores(test=test)
    validate_test_structure(test=test)


__all__ = [
    "validate_test",
    "validate_test_attempt_settings",
    "validate_test_scores",
    "validate_test_structure",
]
