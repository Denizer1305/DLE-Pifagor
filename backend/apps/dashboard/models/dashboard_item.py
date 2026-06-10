from __future__ import annotations

from datetime import datetime, time

from apps.core.models import TimeStampedModel
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class DashboardItem(TimeStampedModel):
    class KindChoices(models.TextChoices):
        CALENDAR = "calendar", _("Событие календаря")
        NOTE = "note", _("Заметка")

    class ThemeChoices(models.TextChoices):
        LESSON = "lesson", _("Урок или занятие")
        CHECKING = "checking", _("Проверка работ")
        DEADLINE = "deadline", _("Дедлайн")
        SYSTEM = "system", _("Организационное событие")
        NEUTRAL = "neutral", _("Другое")

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="dashboard_items",
        verbose_name=_("Пользователь"),
    )
    kind = models.CharField(
        _("Тип"),
        max_length=16,
        choices=KindChoices.choices,
        db_index=True,
    )
    title = models.CharField(_("Заголовок"), max_length=255)
    text = models.TextField(_("Описание"), blank=True)
    item_date = models.DateField(_("Дата"), db_index=True)
    event_theme = models.CharField(
        _("Тема события"),
        max_length=16,
        choices=ThemeChoices.choices,
        default=ThemeChoices.NEUTRAL,
    )
    notification_enabled = models.BooleanField(
        _("Создавать уведомление"),
        default=True,
    )

    class Meta:
        db_table = "dashboard_item"
        verbose_name = _("Элемент личного кабинета")
        verbose_name_plural = _("Элементы личного кабинета")
        ordering = ("-item_date", "-created_at")
        indexes = [
            models.Index(
                fields=["user", "kind", "item_date"],
                name="dash_item_user_kind_date_idx",
            ),
        ]

    @property
    def starts_at(self):
        return timezone.make_aware(datetime.combine(self.item_date, time.min))

    @property
    def remind_at(self):
        return self.starts_at

    def __str__(self) -> str:
        return self.title
