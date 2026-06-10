from __future__ import annotations

from apps.testing.constants import (
    GRADE_SOURCE_CHOICES,
    LEARNER_RESULT_STATUS_CHOICES,
    GradeSource,
    LearnerResultStatus,
)
from apps.testing.managers import TestLearnerResultManager
from django.conf import settings
from django.db import models


class TestLearnerResult(models.Model):
    """
    Итоговый результат обучающегося по тесту.
    """

    test = models.ForeignKey(
        "testing.Test",
        on_delete=models.CASCADE,
        related_name="learner_results",
        verbose_name="Тест",
    )
    learner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="test_results",
        verbose_name="Обучающийся",
    )

    status = models.CharField(
        max_length=32,
        choices=LEARNER_RESULT_STATUS_CHOICES,
        default=LearnerResultStatus.ACTIVE,
    )
    grade_source = models.CharField(
        max_length=32,
        choices=GRADE_SOURCE_CHOICES,
        default=GradeSource.AVERAGE,
    )

    confirmed_attempts_count = models.PositiveSmallIntegerField(default=0)
    attempts_count = models.PositiveSmallIntegerField(default=0)

    average_score = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    average_grade = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
    )
    best_score = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    best_grade = models.PositiveSmallIntegerField(null=True, blank=True)

    last_attempt = models.ForeignKey(
        "testing.TestAttempt",
        on_delete=models.SET_NULL,
        related_name="result_as_last_attempt",
        null=True,
        blank=True,
    )

    is_passed = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_visible_to_learner = models.BooleanField(default=False)
    is_visible_to_guardian = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TestLearnerResultManager()

    class Meta:
        verbose_name = "Итоговый результат теста"
        verbose_name_plural = "Итоговые результаты тестов"
        ordering = ("-updated_at", "-id")
        constraints = (
            models.UniqueConstraint(
                fields=("test", "learner"),
                name="uq_tst_result_learner",
            ),
        )
        indexes = (
            models.Index(fields=("test", "learner"), name="tst_result_user_idx"),
            models.Index(fields=("status",), name="tst_result_status_idx"),
            models.Index(fields=("is_blocked",), name="tst_result_blocked_idx"),
            models.Index(
                fields=("is_visible_to_learner",), name="tst_result_visible_idx"
            ),
        )

    def __str__(self) -> str:
        """
        Возвращает строковое представление результата.
        """

        return f"{self.test} — {self.learner}"

    def clean(self) -> None:
        """
        Запускает доменную валидацию итогового результата.
        """

        from apps.testing.validators import validate_result

        validate_result(result=self)
