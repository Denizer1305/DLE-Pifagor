from __future__ import annotations

from apps.core.models import TimeStampedModel
from django.db import models
from django.utils.translation import gettext_lazy as _


class Organization(TimeStampedModel):
    """
    Образовательная организация.

    Используется для привязки пользователей, групп, отделений,
    учебных предметов и публичной страницы преподавателей.
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
    slug = models.SlugField(
        _("Slug"),
        max_length=160,
        unique=True,
        db_index=True,
        blank=True,
        help_text=_("Человекочитаемый идентификатор для публичных URL."),
    )
    code = models.CharField(
        _("Код организации"),
        max_length=64,
        unique=True,
        db_index=True,
    )

    description = models.TextField(
        _("Описание"),
        blank=True,
    )
    city = models.CharField(
        _("Город"),
        max_length=150,
        blank=True,
    )
    address = models.CharField(
        _("Адрес"),
        max_length=255,
        blank=True,
    )
    phone = models.CharField(
        _("Телефон"),
        max_length=32,
        blank=True,
    )
    email = models.EmailField(
        _("Email"),
        blank=True,
    )
    website = models.URLField(
        _("Сайт"),
        blank=True,
    )
    logo = models.ImageField(
        _("Логотип"),
        upload_to="organizations/logos/%Y/%m/",
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(
        _("Активна"),
        default=True,
    )
    is_public = models.BooleanField(
        _("Показывать публично"),
        default=True,
        db_index=True,
    )
    is_default_public = models.BooleanField(
        _("Организация по умолчанию для публичной зоны"),
        default=False,
        db_index=True,
        help_text=_(
            "Используется для незарегистрированных пользователей на странице преподавателей."
        ),
    )

    class Meta:
        db_table = "organizations_organization"
        verbose_name = _("Образовательная организация")
        verbose_name_plural = _("Образовательные организации")
        ordering = ("name",)
        constraints = [
            models.UniqueConstraint(
                fields=["name"],
                name="organizations_organization_unique_name",
            ),
            models.UniqueConstraint(
                fields=["is_default_public"],
                condition=models.Q(is_default_public=True),
                name="organizations_organization_single_default_public",
            ),
        ]
        indexes = [
            models.Index(
                fields=["is_active", "is_public"],
                name="organizations_org_public_idx",
            ),
            models.Index(
                fields=["is_default_public", "is_active"],
                name="organizations_org_default_idx",
            ),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление организации.

        Returns:
            str: Краткое или полное название организации.
        """

        return self.short_name or self.name

    def save(self, *args, **kwargs) -> None:
        """
        Сохраняет организацию.

        Если slug не задан вручную, использует code.
        """

        if not self.slug and self.code:
            self.slug = self.code.lower().replace("_", "-")

        super().save(*args, **kwargs)
