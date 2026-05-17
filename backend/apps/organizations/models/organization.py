from __future__ import annotations

from apps.core.models import TimeStampedModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Organization(TimeStampedModel):
    """
    Образовательная организация.

    Минимальная модель нужна уже сейчас, потому что users/
    ссылается на организацию в профилях, ролях, заявках и кодах приглашения.
    """

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
        _("Код организации"),
        max_length=64,
        unique=True,
        db_index=True,
    )
    is_active = models.BooleanField(
        _("Активна"),
        default=True,
    )

    class Meta:
        db_table = "organizations_organization"
        verbose_name = _("Образовательная организация")
        verbose_name_plural = _("Образовательные организации")
        ordering = ("name",)

    def __str__(self) -> str:
        """
        Возвращает строковое представление организации.

        Returns:
            str: Краткое или полное название организации.
        """

        return self.short_name or self.name
