from __future__ import annotations

from apps.core.models import TimeStampedModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Subject(TimeStampedModel):
    """
    Учебный предмет.

    Используется на странице преподавателей, в курсах,
    расписании, журнале и учебных материалах.
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
        db_index=True,
    )

    class Meta:
        db_table = "organizations_subject"
        verbose_name = _("Учебный предмет")
        verbose_name_plural = _("Учебные предметы")
        ordering = ("name",)
        indexes = [
            models.Index(
                fields=["is_active", "name"],
                name="org_subj_active_idx",
            ),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление предмета.

        Returns:
            str: Краткое или полное название предмета.
        """

        return self.short_name or self.name
