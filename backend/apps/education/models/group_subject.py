from __future__ import annotations

from apps.education.managers import GroupSubjectManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class GroupSubject(models.Model):
    """
    Предмет учебной группы.

    Фиксирует, какой предмет изучает конкретная учебная группа
    в конкретном учебном году и учебном периоде.
    """

    class AssessmentTypeChoices(models.TextChoices):
        NONE = "none", _("Без аттестации")
        PASS_FAIL = "pass_fail", _("Зачёт / незачёт")
        CREDIT = "credit", _("Зачёт")
        EXAM = "exam", _("Экзамен")
        TEST = "test", _("Тестирование")
        PROJECT = "project", _("Проект")
        OTHER = "other", _("Иная форма")

    group = models.ForeignKey(
        "organizations.StudyGroup",
        on_delete=models.CASCADE,
        related_name="group_subjects",
        verbose_name=_("Учебная группа"),
    )
    subject = models.ForeignKey(
        "organizations.Subject",
        on_delete=models.PROTECT,
        related_name="group_subjects",
        verbose_name=_("Предмет"),
    )
    academic_year = models.ForeignKey(
        "education.AcademicYear",
        on_delete=models.PROTECT,
        related_name="group_subjects",
        verbose_name=_("Учебный год"),
    )
    period = models.ForeignKey(
        "education.EducationPeriod",
        on_delete=models.PROTECT,
        related_name="group_subjects",
        verbose_name=_("Учебный период"),
    )
    curriculum_item = models.ForeignKey(
        "education.CurriculumItem",
        on_delete=models.SET_NULL,
        related_name="group_subjects",
        verbose_name=_("Элемент учебного плана"),
        blank=True,
        null=True,
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
        _("Обязательный предмет"),
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

    objects = GroupSubjectManager()

    class Meta:
        db_table = "education_group_subject"
        verbose_name = _("Предмет группы")
        verbose_name_plural = _("Предметы групп")
        ordering = ("group", "period__sequence", "subject")
        constraints = [
            models.UniqueConstraint(
                fields=("group", "subject", "academic_year", "period"),
                name="education_unique_group_subject_per_period",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.group} — {self.subject} — {self.period}"

    def clean(self) -> None:
        """
        Проверяет согласованность предмета учебной группы.
        """

        super().clean()

        errors: dict[str, str] = {}

        if (
            self.period_id
            and self.academic_year_id
            and self.period.academic_year_id != self.academic_year_id
        ):
            errors["period"] = _(
                "Учебный период должен принадлежать тому же учебному году."
            )

        if self.group_id:
            if hasattr(self.group, "is_active") and not self.group.is_active:
                errors["group"] = _("Нельзя назначить предмет неактивной группе.")

            group_status = getattr(self.group, "status", "")
            if group_status and group_status != "active":
                errors["group"] = _(
                    "Нельзя назначить предмет группе, которая не находится в активном статусе."
                )

            group_academic_year = getattr(self.group, "academic_year", "")
            if (
                group_academic_year
                and self.academic_year_id
                and group_academic_year != self.academic_year.name
            ):
                errors["academic_year"] = _(
                    "Учебный год предмета группы должен совпадать с учебным годом группы."
                )

        if self.subject_id and hasattr(self.subject, "is_active"):
            if not self.subject.is_active:
                errors["subject"] = _("Нельзя назначить неактивный предмет.")

        if self.curriculum_item_id:
            curriculum_item = self.curriculum_item

            if self.subject_id and curriculum_item.subject_id != self.subject_id:
                errors["curriculum_item"] = _(
                    "Элемент учебного плана должен относиться к тому же предмету."
                )

            if self.period_id and curriculum_item.period_id != self.period_id:
                errors["curriculum_item"] = _(
                    "Элемент учебного плана должен относиться к тому же периоду."
                )

            if (
                self.academic_year_id
                and curriculum_item.curriculum.academic_year_id != self.academic_year_id
            ):
                errors["curriculum_item"] = _(
                    "Учебный план элемента должен относиться к тому же учебному году."
                )

            if (
                self.group_id
                and curriculum_item.curriculum.organization_id
                != self.group.organization_id
            ):
                errors["curriculum_item"] = _(
                    "Учебный план элемента должен принадлежать организации группы."
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
