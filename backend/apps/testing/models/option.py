from __future__ import annotations

from apps.testing.managers import TestQuestionOptionManager
from django.db import models


class TestQuestionOption(models.Model):
    """
    Вариант ответа на вопрос теста.
    """

    question = models.ForeignKey(
        "testing.TestQuestion",
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name="Вопрос",
    )

    text = models.TextField(
        verbose_name="Текст варианта",
    )
    order = models.PositiveIntegerField(
        default=1,
        verbose_name="Порядок",
    )

    is_correct = models.BooleanField(
        default=False,
        verbose_name="Правильный ответ",
    )
    score = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
        verbose_name="Балл за вариант",
    )
    feedback = models.TextField(
        blank=True,
        verbose_name="Пояснение к варианту",
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )

    objects = TestQuestionOptionManager()

    class Meta:
        verbose_name = "Вариант ответа"
        verbose_name_plural = "Варианты ответов"
        ordering = (
            "question_id",
            "order",
            "id",
        )
        constraints = (
            models.UniqueConstraint(
                fields=("question", "order"),
                name="uq_tst_option_order",
            ),
        )
        indexes = (
            models.Index(fields=("question",), name="tst_option_question_idx"),
            models.Index(fields=("is_correct",), name="tst_option_correct_idx"),
            models.Index(fields=("is_active",), name="tst_option_active_idx"),
        )

    def __str__(self) -> str:
        """
        Возвращает краткое представление варианта ответа.
        """

        return self.text[:80]
