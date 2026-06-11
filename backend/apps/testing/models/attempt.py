from __future__ import annotations

from apps.testing.constants import (
    ATTEMPT_CHECK_STATUS_CHOICES,
    TEST_ATTEMPT_STATUS_CHOICES,
    AttemptCheckStatus,
    TestAttemptStatus,
)
from apps.testing.managers import TestAttemptManager
from django.conf import settings
from django.db import models


class TestAttempt(models.Model):
    """
    Попытка прохождения теста.
    """

    test = models.ForeignKey(
        "testing.Test",
        on_delete=models.CASCADE,
        related_name="attempts",
        verbose_name="Тест",
    )
    learner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="test_attempts",
        verbose_name="Обучающийся",
    )

    attempt_number = models.PositiveSmallIntegerField(
        verbose_name="Номер попытки",
    )
    status = models.CharField(
        max_length=32,
        choices=TEST_ATTEMPT_STATUS_CHOICES,
        default=TestAttemptStatus.STARTED,
        verbose_name="Статус",
    )
    check_status = models.CharField(
        max_length=32,
        choices=ATTEMPT_CHECK_STATUS_CHOICES,
        default=AttemptCheckStatus.NOT_CHECKED,
        verbose_name="Статус проверки",
    )

    started_at = models.DateTimeField(null=True, blank=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    auto_checked_at = models.DateTimeField(null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)

    expires_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Время истечения попытки",
    )
    expired_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата истечения попытки",
    )

    auto_score = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name="Автоматический балл",
    )
    teacher_score = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Балл преподавателя",
    )
    final_score = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Итоговый балл",
    )

    auto_grade = models.PositiveSmallIntegerField(null=True, blank=True)
    teacher_grade = models.PositiveSmallIntegerField(null=True, blank=True)
    final_grade = models.PositiveSmallIntegerField(null=True, blank=True)

    requires_manual_review = models.BooleanField(default=False)
    is_confirmed_by_teacher = models.BooleanField(default=False)
    is_visible_to_learner = models.BooleanField(default=False)
    is_visible_to_guardian = models.BooleanField(default=False)

    reviewer_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="reviewed_test_attempts",
        null=True,
        blank=True,
        verbose_name="Проверил преподаватель",
    )
    teacher_comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TestAttemptManager()

    class Meta:
        verbose_name = "Попытка теста"
        verbose_name_plural = "Попытки тестов"
        ordering = ("-created_at", "-id")
        constraints = (
            models.UniqueConstraint(
                fields=("test", "learner", "attempt_number"),
                name="uq_tst_attempt_number",
            ),
        )
        indexes = (
            models.Index(fields=("test", "learner"), name="tst_attempt_user_idx"),
            models.Index(fields=("status",), name="tst_attempt_status_idx"),
            models.Index(fields=("check_status",), name="tst_attempt_check_idx"),
            models.Index(
                fields=("is_confirmed_by_teacher",), name="tst_attempt_conf_idx"
            ),
            models.Index(fields=("is_visible_to_learner",), name="tst_attempt_vis_idx"),
            models.Index(fields=("expires_at",), name="tst_attempt_expires_idx"),
        )

    def __str__(self) -> str:
        """
        Возвращает строковое представление попытки.
        """

        return f"{self.test} — попытка {self.attempt_number}"

    def clean(self) -> None:
        """
        Запускает базовую доменную валидацию попытки.
        """

        from apps.testing.validators import (
            validate_attempt_number,
            validate_confirmation_values,
        )

        if self.test_id:
            validate_attempt_number(
                attempt_number=self.attempt_number,
                test=self.test,
            )

            if self.is_confirmed_by_teacher:
                validate_confirmation_values(
                    final_score=self.final_score,
                    final_grade=self.final_grade,
                    max_score=self.test.max_score,
                )
