from __future__ import annotations

from apps.education.managers import CurriculumManager
from apps.education.validators import validate_curriculum_code
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class Curriculum(models.Model):
    """
    Учебный план.

    Описывает академическую структуру подготовки внутри организации
    и учебного года. Может быть привязан к отделению.
    """

    class StatusChoices(models.TextChoices):
        DRAFT = "draft", _("Черновик")
        ACTIVE = "active", _("Активен")
        ARCHIVED = "archived", _("Архивирован")

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="curricula",
        verbose_name=_("Организация"),
    )
    department = models.ForeignKey(
        "organizations.Department",
        on_delete=models.SET_NULL,
        related_name="curricula",
        verbose_name=_("Отделение"),
        blank=True,
        null=True,
    )
    academic_year = models.ForeignKey(
        "education.AcademicYear",
        on_delete=models.PROTECT,
        related_name="curricula",
        verbose_name=_("Учебный год"),
    )

    code = models.CharField(
        _("Код учебного плана"),
        max_length=64,
        validators=[validate_curriculum_code],
    )
    name = models.CharField(
        _("Название учебного плана"),
        max_length=255,
    )
    description = models.TextField(
        _("Описание"),
        blank=True,
    )

    total_hours = models.PositiveIntegerField(
        _("Общее количество часов"),
        blank=True,
        null=True,
        help_text=_("Можно оставить пустым и считать сумму по элементам плана."),
    )

    status = models.CharField(
        _("Статус"),
        max_length=32,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
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

    objects = CurriculumManager()

    class Meta:
        db_table = "education_curriculum"
        verbose_name = _("Учебный план")
        verbose_name_plural = _("Учебные планы")
        ordering = ("organization", "-academic_year__start_date", "name")
        constraints = [
            models.UniqueConstraint(
                fields=("organization", "academic_year", "code"),
                name="education_unique_curriculum_code_per_org_year",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.organization} — {self.name}"

    @property
    def calculated_total_hours(self) -> int:
        """
        Возвращает сумму плановых часов по элементам учебного плана.
        """

        if not self.pk:
            return 0

        return (
            self.items.filter(is_active=True).aggregate(
                total=models.Sum("planned_hours")
            )["total"]
            or 0
        )

    def clean(self) -> None:
        """
        Проверяет принадлежность отделения организации.
        """

        super().clean()

        if (
            self.department_id
            and self.organization_id
            and self.department.organization_id != self.organization_id
        ):
            raise ValidationError(
                {
                    "department": _(
                        "Отделение должно принадлежать той же организации, что и учебный план."
                    )
                }
            )
