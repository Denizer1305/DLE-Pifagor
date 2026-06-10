from __future__ import annotations

from apps.core.models import TimeStampedModel
from apps.organizations.managers import GroupCuratorManager
from apps.organizations.validators import validate_date_range
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class GroupCurator(TimeStampedModel):
    """
    Куратор учебной группы.

    Модель хранит связь между пользователем-преподавателем и учебной группой.
    Проверка роли пользователя выполняется в service-слое, чтобы модель
    не зависела от users.UserRole и не создавала циклические импорты.
    """

    objects = GroupCuratorManager()

    group = models.ForeignKey(
        "organizations.StudyGroup",
        on_delete=models.CASCADE,
        related_name="curators",
        verbose_name=_("Учебная группа"),
    )
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="curated_groups",
        verbose_name=_("Куратор"),
    )
    is_primary = models.BooleanField(
        _("Основной куратор"),
        default=False,
    )
    is_active = models.BooleanField(
        _("Активен"),
        default=True,
    )
    starts_at = models.DateField(
        _("Дата начала кураторства"),
        blank=True,
        null=True,
    )
    ends_at = models.DateField(
        _("Дата окончания кураторства"),
        blank=True,
        null=True,
    )
    notes = models.TextField(
        _("Заметки"),
        blank=True,
    )

    class Meta:
        db_table = "organizations_group_curator"
        verbose_name = _("Куратор группы")
        verbose_name_plural = _("Кураторы групп")
        ordering = ("group", "-is_primary", "teacher")
        constraints = [
            models.UniqueConstraint(
                fields=["group", "teacher"],
                name="organizations_group_curator_unique_teacher",
            ),
        ]
        indexes = [
            models.Index(
                fields=["group", "is_active"],
                name="org_group_curator_active_idx",
            ),
            models.Index(
                fields=["teacher", "is_active"],
                name="org_curator_teacher_active_idx",
            ),
            models.Index(
                fields=["group", "is_primary"],
                name="org_group_curator_primary_idx",
            ),
        ]

    def __str__(self) -> str:
        """
        Возвращает строковое представление куратора группы.

        Returns:
            str: Куратор и группа.
        """

        return f"{self.teacher} — {self.group}"

    @property
    def is_current(self) -> bool:
        """
        Проверяет, является ли кураторство текущим.

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
        Проверяет корректность связи куратора и группы.
        """

        super().clean()

        validate_date_range(
            starts_at=self.starts_at,
            ends_at=self.ends_at,
            field_name="ends_at",
            message="Дата окончания кураторства не может быть раньше даты начала.",
        )

        if self.is_primary and not self.is_active:
            raise ValidationError(
                {"is_primary": _("Основной куратор должен быть активным.")}
            )
