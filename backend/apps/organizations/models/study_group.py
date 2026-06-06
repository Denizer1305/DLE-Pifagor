from __future__ import annotations

from apps.core.models import TimeStampedModel
from apps.organizations.constants import (
    MAX_COURSE_NUMBER,
    MIN_COURSE_NUMBER,
    StudyForm,
    StudyGroupStatus,
)
from apps.organizations.managers import StudyGroupManager
from apps.organizations.validators import validate_year_order
from apps.organizations.models.mixins import GroupJoinCodeMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class StudyGroup(GroupJoinCodeMixin, TimeStampedModel):
    """
    Учебная группа или класс.

    Используется для прикрепления учащихся, кураторов,
    расписания, журнала и заявок.
    """

    objects = StudyGroupManager()

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="study_groups",
        verbose_name=_("Образовательная организация"),
    )
    department = models.ForeignKey(
        "organizations.Department",
        on_delete=models.SET_NULL,
        related_name="study_groups",
        verbose_name=_("Отделение"),
        blank=True,
        null=True,
    )
    name = models.CharField(
        _("Название"),
        max_length=120,
    )
    code = models.CharField(
        _("Код группы"),
        max_length=64,
        blank=True,
        db_index=True,
    )
    admission_year = models.PositiveSmallIntegerField(
        _("Год поступления"),
        blank=True,
        null=True,
    )
    graduation_year = models.PositiveSmallIntegerField(
        _("Год выпуска"),
        blank=True,
        null=True,
    )
    course_number = models.PositiveSmallIntegerField(
        _("Курс"),
        blank=True,
        null=True,
    )
    study_form = models.CharField(
        _("Форма обучения"),
        max_length=32,
        choices=StudyForm.choices,
        default=StudyForm.FULL_TIME,
    )
    status = models.CharField(
        _("Статус"),
        max_length=32,
        choices=StudyGroupStatus.choices,
        default=StudyGroupStatus.ACTIVE,
        db_index=True,
    )
    description = models.TextField(
        _("Описание"),
        blank=True,
    )
    is_active = models.BooleanField(
        _("Активна"),
        default=True,
    )
    is_archived = models.BooleanField(
        _("В архиве"),
        default=False,
    )

    class Meta:
        db_table = "organizations_study_group"
        verbose_name = _("Учебная группа")
        verbose_name_plural = _("Учебные группы")
        ordering = ("organization", "name")
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "name"],
                name="organizations_study_group_unique_name",
            ),
            models.UniqueConstraint(
                fields=["organization", "code"],
                condition=~models.Q(code=""),
                name="organizations_study_group_unique_code",
            ),
        ]
        indexes = [
            models.Index(
                fields=["organization", "status"],
                name="org_study_group_status_idx",
            ),
            models.Index(
                fields=["organization", "is_active"],
                name="org_study_group_active_idx",
            ),
            models.Index(
                fields=["department", "status"],
                name="org_sg_dept_status_idx",
            ),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление группы.

        Returns:
            str: Название группы.
        """

        return self.name

    def clean(self) -> None:
        """
        Проверяет согласованность учебной группы.
        """

        super().clean()

        if (
            self.department_id
            and self.department
            and self.department.organization_id != self.organization_id
        ):
            raise ValidationError(
                {
                    "department": _(
                        "Отделение должно принадлежать выбранной организации."
                    )
                }
            )

        validate_year_order(
            start_year=self.admission_year,
            end_year=self.graduation_year,
            field_name="graduation_year",
            message="Год выпуска не может быть раньше года поступления.",
        )

        if self.course_number is not None and not (
            MIN_COURSE_NUMBER <= self.course_number <= MAX_COURSE_NUMBER
        ):
            raise ValidationError(
                {
                    "course_number": _(
                        "Номер курса должен быть в допустимом диапазоне."
                    )
                }
            )

    def save(self, *args, **kwargs) -> None:
        """
        Сохраняет группу и синхронизирует архивное состояние.
        """

        self.is_archived = self.status == StudyGroupStatus.ARCHIVED
        self.is_active = self.status == StudyGroupStatus.ACTIVE

        super().save(*args, **kwargs)
