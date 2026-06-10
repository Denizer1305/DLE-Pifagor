from __future__ import annotations

from apps.core.models import TimeStampedModel
from apps.organizations.managers import DepartmentManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class Department(TimeStampedModel):
    """
    Отделение образовательной организации.

    Например:
        - отделение информационных технологий;
        - строительное отделение;
        - экономическое отделение.
    """

    objects = DepartmentManager()

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="departments",
        verbose_name=_("Образовательная организация"),
    )
    name = models.CharField(
        _("Название"),
        max_length=255,
    )
    short_name = models.CharField(
        _("Краткое название"),
        max_length=120,
        blank=True,
    )
    code = models.CharField(
        _("Код отделения"),
        max_length=64,
        blank=True,
        db_index=True,
    )
    description = models.TextField(
        _("Описание"),
        blank=True,
    )
    is_active = models.BooleanField(
        _("Активно"),
        default=True,
    )

    class Meta:
        db_table = "organizations_department"
        verbose_name = _("Отделение")
        verbose_name_plural = _("Отделения")
        ordering = ("organization", "name")
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "name"],
                name="organizations_department_unique_name",
            ),
            models.UniqueConstraint(
                fields=["organization", "code"],
                condition=~models.Q(code=""),
                name="organizations_department_unique_code",
            ),
        ]
        indexes = [
            models.Index(
                fields=["organization", "is_active"],
                name="org_department_active_idx",
            ),
            models.Index(
                fields=["organization", "code"],
                name="org_department_code_idx",
            ),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление отделения.

        Returns:
            str: Название отделения.
        """

        return self.short_name or self.name
