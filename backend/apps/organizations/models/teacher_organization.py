from __future__ import annotations

from apps.core.models import TimeStampedModel
from apps.organizations.constants import TeacherEmploymentType
from apps.organizations.validators import validate_date_range
from apps.organizations.managers import TeacherOrganizationManager
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TeacherOrganization(TimeStampedModel):
    """
    Связь преподавателя с образовательной организацией.

    Модель хранит факт принадлежности преподавателя к организации.
    Проверка роли пользователя выполняется в service-слое через UserRole.
    """

    objects = TeacherOrganizationManager()

    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="teacher_organizations",
        verbose_name=_("Преподаватель"),
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="teacher_organizations",
        verbose_name=_("Образовательная организация"),
    )
    position = models.CharField(
        _("Должность"),
        max_length=150,
        blank=True,
    )
    employment_type = models.CharField(
        _("Тип занятости"),
        max_length=32,
        choices=TeacherEmploymentType.choices,
        default=TeacherEmploymentType.FULL_TIME,
    )
    is_primary = models.BooleanField(
        _("Основная организация"),
        default=False,
    )
    is_active = models.BooleanField(
        _("Активна"),
        default=True,
    )
    starts_at = models.DateField(
        _("Дата начала работы"),
        blank=True,
        null=True,
    )
    ends_at = models.DateField(
        _("Дата окончания работы"),
        blank=True,
        null=True,
    )
    notes = models.TextField(
        _("Заметки"),
        blank=True,
    )

    class Meta:
        db_table = "organizations_teacher_organization"
        verbose_name = _("Организация преподавателя")
        verbose_name_plural = _("Организации преподавателей")
        ordering = ("teacher", "-is_primary", "organization")
        constraints = [
            models.UniqueConstraint(
                fields=["teacher", "organization"],
                name="organizations_teacher_org_unique_teacher",
            ),
        ]
        indexes = [
            models.Index(
                fields=["teacher", "is_active"],
                name="org_teacher_org_teacher_idx",
            ),
            models.Index(
                fields=["organization", "is_active"],
                name="org_teacher_org_active_idx",
            ),
            models.Index(
                fields=["teacher", "is_primary"],
                name="org_teacher_org_primary_idx",
            ),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление связи преподавателя и организации.

        Returns:
            str: Преподаватель и организация.
        """

        return f"{self.teacher} — {self.organization}"

    @property
    def is_current(self) -> bool:
        """
        Проверяет, является ли связь преподавателя с организацией текущей.

        Returns:
            bool: True, если связь активна и попадает в диапазон дат.
        """

        if not self.is_active:
            return False

        today = timezone.localdate()

        if self.starts_at and self.starts_at > today:
            return False

        if self.ends_at and self.ends_at < today:
            return False

        return True

    def clean(self) -> None:
        """
        Проверяет корректность связи преподавателя с организацией.
        """

        super().clean()

        validate_date_range(
            starts_at=self.starts_at,
            ends_at=self.ends_at,
            field_name="ends_at",
            message="Дата окончания работы не может быть раньше даты начала.",
        )

        if self.is_primary and not self.is_active:
            raise ValidationError(
                {
                    "is_primary": _(
                        "Основная организация преподавателя должна быть активной."
                    )
                }
            )

        if self.is_primary and self.is_active:
            existing_primary = TeacherOrganization.objects.filter(
                teacher=self.teacher,
                is_primary=True,
                is_active=True,
            )

            if self.pk:
                existing_primary = existing_primary.exclude(pk=self.pk)

            if existing_primary.exists():
                raise ValidationError(
                    {
                        "is_primary": _(
                            "У преподавателя уже есть основная активная организация."
                        )
                    }
                )