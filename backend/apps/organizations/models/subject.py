from __future__ import annotations

from apps.core.models import TimeStampedModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Subject(TimeStampedModel):
    """
    Учебный предмет.

    Используется как справочник предметов для преподавателей,
    групп, учебных планов и заданий.
    """

    name = models.CharField(
        _("Название"),
        max_length=255,
        unique=True,
    )
    short_name = models.CharField(
        _("Краткое название"),
        max_length=120,
        blank=True,
    )
    code = models.CharField(
        _("Код предмета"),
        max_length=64,
        unique=True,
        db_index=True,
    )
    description = models.TextField(
        _("Описание"),
        blank=True,
    )
    is_active = models.BooleanField(
        _("Активен"),
        default=True,
    )

    class Meta:
        db_table = "organizations_subject"
        verbose_name = _("Предмет")
        verbose_name_plural = _("Предметы")
        ordering = ("name",)
        indexes = [
            models.Index(
                fields=["is_active", "name"],
                name="org_subject_active_name_idx",
            ),
            models.Index(
                fields=["code", "is_active"],
                name="org_subject_code_active_idx",
            ),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление предмета.

        Returns:
            str: Краткое или полное название предмета.
        """

        return self.short_name or self.name
