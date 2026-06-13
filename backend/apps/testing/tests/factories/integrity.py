from __future__ import annotations

from apps.testing.constants import IntegrityRiskLevel
from apps.testing.models import TestAttemptIntegrityReport
from apps.testing.tests.factories.attempts import create_attempt


def create_integrity_report(
    *,
    attempt=None,
    **overrides,
) -> TestAttemptIntegrityReport:
    """
    Создаёт сохранённый отчёт добросовестности попытки.
    """

    attempt = attempt or create_attempt()

    data = {
        "attempt": attempt,
        "score": overrides.pop("score", 0),
        "risk_level": overrides.pop(
            "risk_level",
            IntegrityRiskLevel.LOW,
        ),
        "flags_data": overrides.pop("flags_data", []),
    }
    data.update(overrides)

    return TestAttemptIntegrityReport.objects.create(**data)


def create_risky_integrity_report(
    *,
    attempt=None,
    **overrides,
) -> TestAttemptIntegrityReport:
    """
    Создаёт отчёт со средним или высоким риском.
    """

    return create_integrity_report(
        attempt=attempt,
        score=overrides.pop("score", 70),
        risk_level=overrides.pop(
            "risk_level",
            IntegrityRiskLevel.HIGH,
        ),
        flags_data=overrides.pop(
            "flags_data",
            [
                {
                    "code": "too_fast_completion",
                    "title": "Слишком быстрое прохождение",
                    "description": "Попытка отправлена слишком быстро.",
                    "weight": 25,
                }
            ],
        ),
        **overrides,
    )