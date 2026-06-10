from __future__ import annotations

from apps.education.managers import CurriculumItemManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class CurriculumItem(models.Model):
    """
    Элемент учебного плана.

    Описывает предмет, период изучения, часы и форму аттестации
    внутри конкретного учебного плана.
    """

    class AssessmentTypeChoices(models.TextChoices):
        NONE = "none", _("Без аттестации")
        PASS_FAIL = "pass_fail", _("Зачёт / незачёт")
        CREDIT = "credit", _("Зачёт")
        EXAM = "exam", _("Экзамен")
        TEST = "test", _("Тестирование")
        PROJECT = "project", _("Проект")
        OTHER = "other", _("Иная форма")

    curriculum = models.ForeignKey(
        "education.Curriculum",
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name=_("Учебный план"),
    )
    period = models.ForeignKey(
        "education.EducationPeriod",
        on_delete=models.PROTECT,
        related_name="curriculum_items",
        verbose_name=_("Учебный период"),
    )
    subject = models.ForeignKey(
        "organizations.Subject",
        on_delete=models.PROTECT,
        related_name="curriculum_items",
        verbose_name=_("Предмет"),
    )

    sequence = models.PositiveSmallIntegerField(
        _("Порядковый номер"),
        default=1,
    )

    planned_hours = models.PositiveIntegerField(
        _("Плановые часы"),
        default=0,
    )
    contact_hours = models.PositiveIntegerField(
        _("Контактные часы"),
        default=0,
    )
    independent_hours = models.PositiveIntegerField(
        _("Самостоятельная работа"),
        default=0,
    )

    assessment_type = models.CharField(
        _("Форма аттестации"),
        max_length=32,
        choices=AssessmentTypeChoices.choices,
        default=AssessmentTypeChoices.NONE,
    )

    is_required = models.BooleanField(
        _("Обязательный элемент"),
        default=True,
    )
    is_active = models.BooleanField(
        _("Активен"),
        default=True,
    )

    notes = models.TextField(
        _("Примечание"),
        blank=True,
    )

    created_at = models.DateTimeField(
        _("Дата создания"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Дата обновления"),
        auto_now=True,
    )

    objects = CurriculumItemManager()

    class Meta:
        db_table = "education_curriculum_item"
        verbose_name = _("Элемент учебного плана")
        verbose_name_plural = _("Элементы учебного плана")
        ordering = ("curriculum", "period__sequence", "sequence", "subject")
        constraints = [
            models.UniqueConstraint(
                fields=("curriculum", "period", "subject"),
                name="education_unique_subject_per_curriculum_period",
            ),
            models.UniqueConstraint(
                fields=("curriculum", "period", "sequence"),
                name="education_unique_sequence_per_curriculum_period",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.curriculum} — {self.subject} — {self.period}"

    def clean(self) -> None:
        """
        Проверяет согласованность элемента учебного плана.
        """

        super().clean()

        errors: dict[str, str] = {}

        if (
            self.curriculum_id
            and self.period_id
            and self.period.academic_year_id != self.curriculum.academic_year_id
        ):
            errors["period"] = _(
                "Учебный период должен принадлежать тому же учебному году, что и учебный план."
            )

        if self.subject_id and hasattr(self.subject, "is_active"):
            if not self.subject.is_active:
                errors["subject"] = _(
                    "Нельзя добавить неактивный предмет в учебный план."
                )

        if self.contact_hours > self.planned_hours:
            errors["contact_hours"] = _(
                "Контактные часы не могут превышать плановые часы."
            )

        if self.independent_hours > self.planned_hours:
            errors["independent_hours"] = _(
                "Самостоятельные часы не могут превышать плановые часы."
            )

        if (self.contact_hours + self.independent_hours) > self.planned_hours:
            errors["planned_hours"] = _(
                "Сумма контактных и самостоятельных часов не может превышать плановые часы."
            )

        if errors:
            raise ValidationError(errors)
