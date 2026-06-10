from __future__ import annotations

from decimal import ROUND_HALF_UP, Decimal


def calculate_score_percent(
    *,
    score,
    max_score,
) -> Decimal:
    """
    Рассчитывает процент выполнения теста.
    """

    if not max_score:
        return Decimal("0.00")

    percent = Decimal(score) / Decimal(max_score) * Decimal("100")

    return percent.quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )


def calculate_grade_from_score(
    *,
    score,
    max_score,
) -> int:
    """
    Рассчитывает предварительную оценку по баллам.
    """

    percent = calculate_score_percent(
        score=score,
        max_score=max_score,
    )

    if percent >= Decimal("85"):
        return 5

    if percent >= Decimal("70"):
        return 4

    if percent >= Decimal("50"):
        return 3

    return 2
