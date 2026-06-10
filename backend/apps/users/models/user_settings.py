from __future__ import annotations

from apps.core.models import TimeStampedModel
from apps.users.constants.roles import RoleCode
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserSettings(TimeStampedModel):
    """
    Настройки пользователя.

    Хранит персональные настройки интерфейса:
        - язык;
        - часовой пояс;
        - активная роль;
        - возрастная тема интерфейса;
        - компактный режим.

    Настройки уведомлений позже лучше вынести в приложение notifications.
    """

    class InterfaceTheme(models.TextChoices):
        """
        Возрастные и ролевые темы интерфейса.
        """

        DEFAULT = "default", _("По умолчанию")
        JUNIOR = "junior", _("Младшие классы")
        MIDDLE = "middle", _("Средние классы")
        SENIOR = "senior", _("Старшие классы")
        COLLEGE = "college", _("Колледж")
        UNIVERSITY = "university", _("Университет")
        TEACHER = "teacher", _("Преподаватель")
        GUARDIAN = "guardian", _("Родитель")
        ADMIN = "admin", _("Администратор")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="settings",
        verbose_name=_("Пользователь"),
    )

    language = models.CharField(
        _("Язык интерфейса"),
        max_length=16,
        default="ru",
    )
    timezone = models.CharField(
        _("Часовой пояс"),
        max_length=150,
        default="Europe/Moscow",
    )

    active_role = models.CharField(
        _("Активная роль"),
        max_length=64,
        choices=RoleCode.choices,
        blank=True,
    )

    interface_theme = models.CharField(
        _("Тема интерфейса"),
        max_length=32,
        choices=InterfaceTheme.choices,
        default=InterfaceTheme.DEFAULT,
    )

    compact_mode = models.BooleanField(
        _("Компактный режим"),
        default=False,
    )

    appearance_settings = models.JSONField(
        "Настройки внешнего вида",
        default=dict,
        blank=True,
    )
    notification_settings = models.JSONField(
        "Настройки уведомлений",
        default=dict,
        blank=True,
    )
    privacy_settings = models.JSONField(
        "Настройки приватности",
        default=dict,
        blank=True,
    )
    role_settings = models.JSONField(
        "Ролевые настройки интерфейса",
        default=dict,
        blank=True,
    )
    security_settings = models.JSONField(
        "Настройки безопасности",
        default=dict,
        blank=True,
    )

    class Meta:
        db_table = "users_user_settings"
        verbose_name = _("Настройки пользователя")
        verbose_name_plural = _("Настройки пользователей")

    def __str__(self) -> str:
        """
        Возвращает строковое представление настроек.

        Returns:
            str: Настройки пользователя.
        """

        return f"Настройки: {self.user}"
