from __future__ import annotations

from django.db import models


class IntegrityRiskLevel(models.TextChoices):
    """
    Уровень риска по отчёту добросовестности прохождения теста.
    """

    LOW = "low", "Низкий риск"
    MEDIUM = "medium", "Средний риск"
    HIGH = "high", "Высокий риск"


INTEGRITY_RISK_LEVEL_CHOICES = IntegrityRiskLevel.choices
