from __future__ import annotations

from django.db import models


class BankItemStatus(models.TextChoices):
    """
    Статусы шаблона вопроса в банке заданий.
    """

    DRAFT = "draft", "Черновик"
    PUBLISHED = "published", "Опубликован"
    ARCHIVED = "archived", "Архив"


class BankItemVisibility(models.TextChoices):
    """
    Видимость шаблона вопроса.
    """

    PRIVATE = "private", "Только автор"
    ORGANIZATION = "organization", "Организация"
    PUBLIC = "public", "Платформа"


class BankItemDifficulty(models.TextChoices):
    """
    Сложность шаблона вопроса.
    """

    EASY = "easy", "Лёгкий"
    MEDIUM = "medium", "Средний"
    HARD = "hard", "Сложный"


BANK_ITEM_STATUS_CHOICES = BankItemStatus.choices
BANK_ITEM_VISIBILITY_CHOICES = BankItemVisibility.choices
BANK_ITEM_DIFFICULTY_CHOICES = BankItemDifficulty.choices
