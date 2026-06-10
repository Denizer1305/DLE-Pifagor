from __future__ import annotations

from apps.education.constants import FINISHED_ENROLLMENT_STATUS_CODES
from apps.education.managers import LearnerGroupEnrollmentManager
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _


class LearnerGroupEnrollment(models.Model):
    """
    Академическое зачисление обучающегося в учебную группу.

    Это не заявка на вступление. Заявки живут в users/organizations.
    Эта модель фиксирует факт обучения пользователя в группе
    в рамках конкретного учебного года.
    """

    class StatusChoices(models.TextChoices):
        ACTIVE = "active", _("Активно")
        TRANSFERRED = "transferred", _("Переведён")
        SUSPENDED = "suspended", _("Приостановлено")
        GRADUATED = "graduated", _("Завершено")
        EXPELLED = "expelled", _("Отчислен")
        ARCHIVED = "archived", _("Архивировано")

    learner = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="learner_group_enrollments",
        verbose_name=_("Обучающийся"),
    )
    group = models.ForeignKey(
        "organizations.StudyGroup",
        on_delete=models.CASCADE,
        related_name="learner_enrollments",
        verbose_name=_("Учебная группа"),
    )
    academic_year = models.ForeignKey(
        "education.AcademicYear",
        on_delete=models.PROTECT,
        related_name="learner_enrollments",
        verbose_name=_("Учебный год"),
    )

    enrollment_date = models.DateField(
        _("Дата зачисления"),
    )
    completion_date = models.DateField(
        _("Дата завершения / выбытия"),
        blank=True,
        null=True,
    )

    status = models.CharField(
        _("Статус"),
        max_length=32,
        choices=StatusChoices.choices,
        default=StatusChoices.ACTIVE,
    )
    is_primary = models.BooleanField(
        _("Основное зачисление"),
        default=True,
    )

    journal_number = models.PositiveIntegerField(
        _("Номер в журнале"),
        blank=True,
        null=True,
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

    objects = LearnerGroupEnrollmentManager()

    class Meta:
        db_table = "education_learner_group_enrollment"
        verbose_name = _("Зачисление обучающегося в группу")
        verbose_name_plural = _("Зачисления обучающихся в группы")
        ordering = ("-academic_year__start_date", "group", "learner")
        constraints = [
            models.UniqueConstraint(
                fields=("learner", "group", "academic_year"),
                name="education_unique_learner_group_enrollment_per_year",
            ),
            models.UniqueConstraint(
                fields=("learner", "academic_year", "is_primary"),
                condition=Q(is_primary=True),
                name="education_unique_primary_learner_enrollment_per_year",
            ),
            models.UniqueConstraint(
                fields=("group", "academic_year", "journal_number"),
                condition=Q(journal_number__isnull=False),
                name="education_unique_journal_number_per_group_year",
            ),
        ]

    def __str__(self) -> str:
        full_name = getattr(self.learner, "full_name", str(self.learner))

        return f"{full_name} — {self.group} — {self.academic_year}"

    def clean(self) -> None:
        """
        Проверяет согласованность академического зачисления.
        """

        super().clean()

        errors: dict[str, str] = {}

        if self.completion_date and self.enrollment_date:
            if self.completion_date < self.enrollment_date:
                errors["completion_date"] = _(
                    "Дата завершения не может быть раньше даты зачисления."
                )

        if self.academic_year_id and self.enrollment_date:
            if self.enrollment_date < self.academic_year.start_date:
                errors["enrollment_date"] = _(
                    "Дата зачисления не может быть раньше начала учебного года."
                )

            if self.enrollment_date > self.academic_year.end_date:
                errors["enrollment_date"] = _(
                    "Дата зачисления не может быть позже окончания учебного года."
                )

        if self.academic_year_id and self.completion_date:
            if self.completion_date > self.academic_year.end_date:
                errors["completion_date"] = _(
                    "Дата завершения не может быть позже окончания учебного года."
                )

        if self.group_id:
            if hasattr(self.group, "is_active") and not self.group.is_active:
                errors["group"] = _(
                    "Нельзя зачислить обучающегося в неактивную группу."
                )

            group_status = getattr(self.group, "status", "")
            if group_status and group_status != "active":
                errors["group"] = _(
                    "Нельзя зачислить обучающегося в группу, которая не находится в активном статусе."
                )

            group_academic_year = getattr(self.group, "academic_year", "")
            if (
                group_academic_year
                and self.academic_year_id
                and group_academic_year != self.academic_year.name
            ):
                errors["academic_year"] = _(
                    "Учебный год зачисления должен совпадать с учебным годом группы."
                )

        if self.status in FINISHED_ENROLLMENT_STATUS_CODES and not self.completion_date:
            errors["completion_date"] = _(
                "Для завершённого, переведённого, архивного или отчисленного зачисления требуется дата завершения."
            )

        if errors:
            raise ValidationError(errors)
