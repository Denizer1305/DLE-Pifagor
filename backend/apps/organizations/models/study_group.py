from __future__ import annotations

from apps.core.models import TimeStampedModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class StudyGroup(TimeStampedModel):
    """
    Учебная группа или класс.

    Используется для прикрепления учащихся, кураторов,
    расписания, журнала и заявок.
    """

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
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление группы.

        Returns:
            str: Название группы.
        """

        return self.name
