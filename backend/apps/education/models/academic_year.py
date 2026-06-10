from __future__ import annotations

from apps.education.managers import AcademicYearManager
from apps.education.validators import validate_academic_year_name
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class AcademicYear(models.Model):
    """
    Учебный год.

    Базовая академическая сущность для учебных периодов,
    учебных планов, предметов групп и зачислений обучающихся.
    """

    name = models.CharField(
        _("Название учебного года"),
        max_length=32,
        unique=True,
        validators=[validate_academic_year_name],
        help_text=_("Например: 2025/2026."),
    )
    start_date = models.DateField(
        _("Дата начала"),
    )
    end_date = models.DateField(
        _("Дата окончания"),
    )

    description = models.TextField(
        _("Описание"),
        blank=True,
    )

    is_current = models.BooleanField(
        _("Текущий учебный год"),
        default=False,
    )
    is_active = models.BooleanField(
        _("Активен"),
        default=True,
    )

    created_at = models.DateTimeField(
        _("Дата создания"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Дата обновления"),
        auto_now=True,
    )

    objects = AcademicYearManager()

    class Meta:
        db_table = "education_academic_year"
        verbose_name = _("Учебный год")
        verbose_name_plural = _("Учебные годы")
        ordering = ("-start_date",)
        constraints = [
            models.UniqueConstraint(
                fields=("is_current",),
                condition=Q(is_current=True),
                name="education_unique_current_academic_year",
            ),
        ]

    def __str__(self) -> str:
        return self.name

    def clean(self) -> None:
        """
        Проверяет календарные границы учебного года.
        """

        super().clean()

        errors: dict[str, str] = {}

        if self.start_date and self.end_date and self.end_date <= self.start_date:
            errors["end_date"] = _("Дата окончания должна быть позже даты начала.")

        if self.name and self.start_date and self.end_date:
            try:
                start_year, end_year = self.name.split("/")
            except ValueError:
                start_year = ""
                end_year = ""

            if start_year and int(start_year) != self.start_date.year:
                errors["name"] = _(
                    "Первый год в названии должен совпадать с годом даты начала."
                )

            if end_year and int(end_year) != self.end_date.year:
                errors["name"] = _(
                    "Второй год в названии должен совпадать с годом даты окончания."
                )

        if errors:
            raise ValidationError(errors)
