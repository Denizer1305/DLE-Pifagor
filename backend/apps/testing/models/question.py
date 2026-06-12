from __future__ import annotations

from apps.testing.constants import (
    BANK_ITEM_DIFFICULTY_CHOICES,
    QUESTION_CHECK_MODE_CHOICES,
    QUESTION_TYPE_CHOICES,
    BankItemDifficulty,
    QuestionCheckMode,
    QuestionType,
)
from apps.testing.managers import TestQuestionManager
from django.db import models


class TestQuestion(models.Model):
    """
    Вопрос теста.
    """

    test = models.ForeignKey(
        "testing.Test",
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Тест",
    )

    source_bank_item = models.ForeignKey(
        "testing.QuestionBankItem",
        on_delete=models.SET_NULL,
        related_name="created_test_questions",
        null=True,
        blank=True,
        verbose_name="Источник из банка заданий",
    )

    question_type = models.CharField(
        max_length=32,
        choices=QUESTION_TYPE_CHOICES,
        default=QuestionType.SINGLE_CHOICE,
        verbose_name="Тип вопроса",
    )
    check_mode = models.CharField(
        max_length=32,
        choices=QUESTION_CHECK_MODE_CHOICES,
        default=QuestionCheckMode.AUTO,
        verbose_name="Режим проверки",
    )

    title = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Краткое название",
    )
    text = models.TextField(
        verbose_name="Текст вопроса",
    )
    explanation = models.TextField(
        blank=True,
        verbose_name="Пояснение",
    )

    expected_text_answer = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Ожидаемый текстовый ответ",
    )
    expected_number_answer = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name="Ожидаемый числовой ответ",
    )
    case_sensitive = models.BooleanField(
        default=False,
        verbose_name="Учитывать регистр",
    )

    order = models.PositiveIntegerField(
        default=1,
        verbose_name="Порядок",
    )
    score = models.PositiveIntegerField(
        default=1,
        verbose_name="Балл",
    )

    difficulty = models.CharField(
        max_length=32,
        choices=BANK_ITEM_DIFFICULTY_CHOICES,
        default=BankItemDifficulty.MEDIUM,
        verbose_name="Сложность",
    )
    tags_data = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Теги",
    )
    is_reusable = models.BooleanField(
        default=False,
        verbose_name="Можно переиспользовать",
    )

    is_required = models.BooleanField(
        default=True,
        verbose_name="Обязательный",
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

    objects = TestQuestionManager()

    class Meta:
        verbose_name = "Вопрос теста"
        verbose_name_plural = "Вопросы тестов"
        ordering = (
            "test_id",
            "order",
            "id",
        )
        constraints = (
            models.UniqueConstraint(
                fields=("test", "order"),
                name="uq_tst_question_order",
            ),
        )
        indexes = (
            models.Index(fields=("test",), name="tst_question_test_idx"),
            models.Index(fields=("question_type",), name="tst_question_type_idx"),
            models.Index(fields=("check_mode",), name="tst_question_check_idx"),
            models.Index(fields=("is_active",), name="tst_question_active_idx"),
            models.Index(fields=("source_bank_item",), name="tst_question_bank_idx"),
            models.Index(fields=("difficulty",), name="tst_question_diff_idx"),
            models.Index(fields=("is_reusable",), name="tst_question_reuse_idx"),
        )

    def __str__(self) -> str:
        """
        Возвращает краткое представление вопроса.
        """

        if self.title:
            return self.title

        return self.text[:80]

    def clean(self) -> None:
        """
        Запускает доменную валидацию вопроса.
        """

        super().clean()

        from apps.testing.validators import validate_question_bank_source

        validate_question_bank_source(question=self)
