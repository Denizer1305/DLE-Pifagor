from __future__ import annotations

from apps.testing.managers import TestAttemptAnswerManager
from django.db import models


class TestAttemptAnswer(models.Model):
    """
    Ответ обучающегося на вопрос теста.
    """

    attempt = models.ForeignKey(
        "testing.TestAttempt",
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Попытка",
    )
    question = models.ForeignKey(
        "testing.TestQuestion",
        on_delete=models.PROTECT,
        related_name="attempt_answers",
        verbose_name="Вопрос",
    )

    selected_option = models.ForeignKey(
        "testing.TestQuestionOption",
        on_delete=models.SET_NULL,
        related_name="single_attempt_answers",
        null=True,
        blank=True,
        verbose_name="Выбранный вариант",
    )
    selected_options_data = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Выбранные варианты",
    )

    text_answer = models.TextField(blank=True)
    number_answer = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
    )

    is_correct = models.BooleanField(
        null=True,
        blank=True,
        verbose_name="Ответ верный",
    )
    auto_score = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    teacher_score = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )
    final_score = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    requires_manual_review = models.BooleanField(default=False)
    teacher_comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TestAttemptAnswerManager()

    class Meta:
        verbose_name = "Ответ на вопрос теста"
        verbose_name_plural = "Ответы на вопросы тестов"
        ordering = ("attempt_id", "question_id", "id")
        constraints = (
            models.UniqueConstraint(
                fields=("attempt", "question"),
                name="uq_tst_answer_question",
            ),
        )
        indexes = (
            models.Index(fields=("attempt",), name="tst_answer_attempt_idx"),
            models.Index(fields=("question",), name="tst_answer_question_idx"),
            models.Index(fields=("selected_option",), name="tst_answer_option_idx"),
            models.Index(
                fields=("requires_manual_review",), name="tst_answer_review_idx"
            ),
        )

    def __str__(self) -> str:
        """
        Возвращает строковое представление ответа.
        """

        return f"{self.attempt} — {self.question}"

    def clean(self) -> None:
        """
        Запускает доменную валидацию ответа.
        """

        from apps.testing.validators import validate_answer

        validate_answer(answer=self)
