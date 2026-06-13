from __future__ import annotations

from apps.testing.constants import (
    BANK_ITEM_DIFFICULTY_CHOICES,
    BANK_ITEM_STATUS_CHOICES,
    BANK_ITEM_VISIBILITY_CHOICES,
    QUESTION_CHECK_MODE_CHOICES,
    QUESTION_TYPE_CHOICES,
    BankItemDifficulty,
    BankItemStatus,
    BankItemVisibility,
    QuestionCheckMode,
    QuestionType,
)
from apps.testing.managers import QuestionBankItemManager, QuestionBankOptionManager
from django.conf import settings
from django.db import models


class QuestionBankItem(models.Model):
    """
    Шаблон вопроса в банке тестовых заданий.
    """

    title = models.CharField(
        max_length=255,
        verbose_name="Название",
    )
    text = models.TextField(
        verbose_name="Текст вопроса",
    )
    explanation = models.TextField(
        blank=True,
        verbose_name="Пояснение",
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

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="question_bank_items",
        verbose_name="Организация",
    )
    subject = models.ForeignKey(
        "organizations.Subject",
        on_delete=models.PROTECT,
        related_name="question_bank_items",
        verbose_name="Предмет",
    )
    owner_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="owned_question_bank_items",
        verbose_name="Преподаватель-владелец",
    )

    visibility = models.CharField(
        max_length=32,
        choices=BANK_ITEM_VISIBILITY_CHOICES,
        default=BankItemVisibility.PRIVATE,
        verbose_name="Видимость",
    )
    status = models.CharField(
        max_length=32,
        choices=BANK_ITEM_STATUS_CHOICES,
        default=BankItemStatus.DRAFT,
        verbose_name="Статус",
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Активен",
    )

    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата публикации",
    )
    archived_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата архивирования",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )

    objects = QuestionBankItemManager()

    class Meta:
        verbose_name = "Шаблон вопроса"
        verbose_name_plural = "Банк тестовых заданий"
        ordering = (
            "-updated_at",
            "-id",
        )
        indexes = (
            models.Index(fields=("status",), name="tst_bank_status_idx"),
            models.Index(fields=("visibility",), name="tst_bank_vis_idx"),
            models.Index(fields=("difficulty",), name="tst_bank_diff_idx"),
            models.Index(fields=("question_type",), name="tst_bank_type_idx"),
            models.Index(fields=("organization",), name="tst_bank_org_idx"),
            models.Index(fields=("subject",), name="tst_bank_subject_idx"),
            models.Index(fields=("owner_teacher",), name="tst_bank_owner_idx"),
            models.Index(fields=("is_active",), name="tst_bank_active_idx"),
        )

    def __str__(self) -> str:
        """
        Возвращает название шаблона вопроса.
        """

        return self.title

    def clean(self) -> None:
        """
        Валидирует шаблон вопроса банка тестовых заданий.
        """

        super().clean()

        from apps.testing.validators import validate_bank_item

        validate_bank_item(item=self)


class QuestionBankOption(models.Model):
    """
    Вариант ответа шаблона вопроса.
    """

    bank_item = models.ForeignKey(
        "testing.QuestionBankItem",
        on_delete=models.CASCADE,
        related_name="options",
        verbose_name="Шаблон вопроса",
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

    objects = QuestionBankOptionManager()

    class Meta:
        verbose_name = "Вариант шаблона вопроса"
        verbose_name_plural = "Варианты шаблонов вопросов"
        ordering = (
            "bank_item_id",
            "order",
            "id",
        )
        constraints = (
            models.UniqueConstraint(
                fields=("bank_item", "order"),
                name="uq_tst_bank_option_order",
            ),
        )
        indexes = (
            models.Index(fields=("bank_item",), name="tst_bank_opt_item_idx"),
            models.Index(fields=("is_correct",), name="tst_bank_opt_corr_idx"),
            models.Index(fields=("is_active",), name="tst_bank_opt_act_idx"),
        )

    def __str__(self) -> str:
        """
        Возвращает краткое представление варианта.
        """

        return self.text[:80]

    def clean(self) -> None:
        """
        Валидирует вариант шаблона вопроса.
        """

        super().clean()

        from apps.testing.validators import validate_bank_option

        validate_bank_option(option=self)
