from __future__ import annotations

from apps.core.models import TimeStampedModel
from apps.core.validators import validate_image_extension
from apps.users.constants.moderation import ModerationStatus
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(TimeStampedModel):
    """
    Базовый профиль пользователя.

    Содержит общие публичные и полупубличные данные:
        - аватар;
        - город;
        - краткое описание;
        - ссылки на социальные профили;
        - статусы модерации.

    Ролевые данные учащегося, родителя и преподавателя
    хранятся в отдельных моделях.
    """

    class GenderChoices(models.TextChoices):
        """
        Варианты пола пользователя.

        Используется как необязательное поле профиля.
        """

        MALE = "male", _("Мужской")
        FEMALE = "female", _("Женский")
        NOT_SPECIFIED = "not_specified", _("Не указан")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("Пользователь"),
    )

    gender = models.CharField(
        _("Пол"),
        max_length=32,
        choices=GenderChoices.choices,
        default=GenderChoices.NOT_SPECIFIED,
    )
    avatar = models.ImageField(
        _("Аватар"),
        upload_to="users/avatars/%Y/%m/",
        validators=[validate_image_extension],
        blank=True,
        null=True,
    )

    about = models.TextField(
        _("О себе"),
        blank=True,
    )
    city = models.CharField(
        _("Город"),
        max_length=150,
        blank=True,
    )
    timezone = models.CharField(
        _("Часовой пояс"),
        max_length=150,
        default="Europe/Moscow",
        blank=True,
    )

    social_link_max = models.URLField(
        _("Ссылка на профиль в MAX"),
        blank=True,
        default="",
    )
    social_link_vk = models.URLField(
        _("Ссылка на профиль во ВКонтакте"),
        blank=True,
        default="",
    )

    avatar_moderation_status = models.CharField(
        _("Статус модерации аватара"),
        max_length=32,
        choices=ModerationStatus.choices,
        default=ModerationStatus.NOT_SUBMITTED,
    )
    profile_moderation_status = models.CharField(
        _("Статус модерации профиля"),
        max_length=32,
        choices=ModerationStatus.choices,
        default=ModerationStatus.NOT_SUBMITTED,
    )
    moderation_comment = models.TextField(
        _("Комментарий модератора"),
        blank=True,
    )

    class Meta:
        db_table = "users_profile"
        verbose_name = _("Профиль")
        verbose_name_plural = _("Профили")
        ordering = ("user__last_name", "user__first_name")

    def __str__(self) -> str:
        """
        Возвращает строковое представление профиля.

        Returns:
            str: Профиль пользователя.
        """

        return f"Профиль: {self.user}"

    def clean(self) -> None:
        """
        Нормализует текстовые поля профиля.
        """

        super().clean()

        if self.about:
            self.about = self.about.strip()

        if self.city:
            self.city = self.city.strip()

        if self.moderation_comment:
            self.moderation_comment = self.moderation_comment.strip()

    def submit_avatar_for_moderation(self, *, save: bool = True) -> None:
        """
        Отправляет аватар на модерацию.

        Args:
            save:
                Нужно ли сразу сохранить изменения.
        """

        self.avatar_moderation_status = ModerationStatus.PENDING

        if save:
            self.save(update_fields=["avatar_moderation_status", "updated_at"])
