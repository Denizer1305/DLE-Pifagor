from __future__ import annotations

from django.db import models
from django.utils import timezone

from apps.testing.constants import (
    INTEGRITY_RISK_LEVEL_CHOICES,
    IntegrityRiskLevel,
)
from apps.testing.managers import TestAttemptIntegrityReportManager


class TestAttemptIntegrityReport(models.Model):
    """
    Сохранённый отчёт о добросовестности прохождения теста.

    Отчёт не является доказательством списывания.
    Он только показывает преподавателю признаки риска.
    """

    attempt = models.OneToOneField(
        "testing.TestAttempt",
        on_delete=models.CASCADE,
        related_name="integrity_report",
        verbose_name="Попытка",
    )

    score = models.PositiveSmallIntegerField(
        default=0,
        verbose_name="Итоговый риск, баллы",
    )
    risk_level = models.CharField(
        max_length=32,
        choices=INTEGRITY_RISK_LEVEL_CHOICES,
        default=IntegrityRiskLevel.LOW,
        verbose_name="Уровень риска",
    )
    flags_data = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Признаки риска",
    )

    checked_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Дата анализа",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )

    objects = TestAttemptIntegrityReportManager()

    class Meta:
        verbose_name = "Отчёт добросовестности попытки"
        verbose_name_plural = "Отчёты добросовестности попыток"
        ordering = (
            "-checked_at",
            "-id",
        )
        indexes = (
            models.Index(fields=("attempt",), name="tst_integrity_att_idx"),
            models.Index(fields=("risk_level",), name="tst_integrity_risk_idx"),
            models.Index(fields=("score",), name="tst_integrity_score_idx"),
            models.Index(fields=("checked_at",), name="tst_integrity_date_idx"),
        )

    def __str__(self) -> str:
        """
        Возвращает строковое представление отчёта.
        """

        return f"{self.attempt} — {self.risk_level}"