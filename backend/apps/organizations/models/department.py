from __future__ import annotations

from apps.core.models import TimeStampedModel
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
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление отделения.

        Returns:
            str: Название отделения.
        """

        return self.short_name or self.name
