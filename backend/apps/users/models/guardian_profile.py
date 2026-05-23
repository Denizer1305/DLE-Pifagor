from __future__ import annotations

from apps.core.models import TimeStampedModel
from apps.core.validators import validate_phone_number
from apps.users.constants.lifecycle import ProfileStatus
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class GuardianProfile(TimeStampedModel):
    """
    Профиль родителя или законного представителя.

    Guardian шире, чем Parent:
        - родитель;
        - опекун;
        - законный представитель.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guardian_profile",
        verbose_name=_("Пользователь"),
    )

    status = models.CharField(
        _("Статус профиля"),
        max_length=32,
        choices=ProfileStatus.choices,
        default=ProfileStatus.DRAFT,
        db_index=True,
    )

    occupation = models.CharField(
        _("Род деятельности"),
        max_length=255,
        blank=True,
    )
    work_place = models.CharField(
        _("Место работы"),
        max_length=255,
        blank=True,
    )
    emergency_contact_phone = models.CharField(
        _("Экстренный телефон для связи"),
        max_length=32,
        validators=[validate_phone_number],
        blank=True,
    )

    notes = models.TextField(
        _("Служебные заметки"),
        blank=True,
        default="",
    )

    class Meta:
        db_table = "users_guardian_profile"
        verbose_name = _("Профиль родителя")
        verbose_name_plural = _("Профили родителей")

    def __str__(self) -> str:
        """
        Возвращает строковое представление профиля родителя.

        Returns:
            str: Пользователь.
        """

        return f"Родитель: {self.user}"

    def clean(self) -> None:
        """
        Нормализует текстовые поля профиля.
        """

        super().clean()

        if self.occupation:
            self.occupation = self.occupation.strip()

        if self.work_place:
            self.work_place = self.work_place.strip()

        if self.notes:
            self.notes = self.notes.strip()
