from __future__ import annotations

from apps.materials.constants import (
    MATERIAL_USAGE_ACTION_ARCHIVE,
    MATERIAL_USAGE_ACTION_ATTACH,
    MATERIAL_USAGE_ACTION_CREATE_VERSION,
    MATERIAL_USAGE_ACTION_DETACH,
    MATERIAL_USAGE_ACTION_DOWNLOAD,
    MATERIAL_USAGE_ACTION_MAX_LENGTH,
    MATERIAL_USAGE_ACTION_OPEN_LINK,
    MATERIAL_USAGE_ACTION_PUBLISH,
    MATERIAL_USAGE_ACTION_UPDATE,
    MATERIAL_USAGE_ACTION_VIEW,
    MATERIAL_USAGE_CONTEXT_ADMIN,
    MATERIAL_USAGE_CONTEXT_ASSIGNMENT,
    MATERIAL_USAGE_CONTEXT_COURSE,
    MATERIAL_USAGE_CONTEXT_LESSON,
    MATERIAL_USAGE_CONTEXT_LIBRARY,
    MATERIAL_USAGE_CONTEXT_MAX_LENGTH,
    MATERIAL_USAGE_CONTEXT_OTHER,
    MATERIAL_USAGE_CONTEXT_PROFILE,
    MATERIAL_USAGE_IP_ADDRESS_MAX_LENGTH,
    MATERIAL_USAGE_USER_AGENT_MAX_LENGTH,
)
from apps.materials.managers import MaterialUsageLogManager
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class MaterialUsageLog(models.Model):
    """
    Журнал использования учебных материалов.

    Используется для истории действий и будущей аналитики:
    просмотры, скачивания, открытия ссылок, прикрепления к курсам и заданиям.
    """

    class ActionChoices(models.TextChoices):
        VIEW = MATERIAL_USAGE_ACTION_VIEW, _("Просмотр")
        DOWNLOAD = MATERIAL_USAGE_ACTION_DOWNLOAD, _("Скачивание")
        OPEN_LINK = MATERIAL_USAGE_ACTION_OPEN_LINK, _("Открытие ссылки")
        ATTACH = MATERIAL_USAGE_ACTION_ATTACH, _("Прикрепление")
        DETACH = MATERIAL_USAGE_ACTION_DETACH, _("Открепление")
        UPDATE = MATERIAL_USAGE_ACTION_UPDATE, _("Обновление")
        CREATE_VERSION = MATERIAL_USAGE_ACTION_CREATE_VERSION, _("Создание версии")
        PUBLISH = MATERIAL_USAGE_ACTION_PUBLISH, _("Публикация")
        ARCHIVE = MATERIAL_USAGE_ACTION_ARCHIVE, _("Архивация")

    class ContextChoices(models.TextChoices):
        LIBRARY = MATERIAL_USAGE_CONTEXT_LIBRARY, _("Библиотека")
        COURSE = MATERIAL_USAGE_CONTEXT_COURSE, _("Курс")
        LESSON = MATERIAL_USAGE_CONTEXT_LESSON, _("Урок")
        ASSIGNMENT = MATERIAL_USAGE_CONTEXT_ASSIGNMENT, _("Задание")
        PROFILE = MATERIAL_USAGE_CONTEXT_PROFILE, _("Профиль")
        ADMIN = MATERIAL_USAGE_CONTEXT_ADMIN, _("Админка")
        OTHER = MATERIAL_USAGE_CONTEXT_OTHER, _("Другое")

    material = models.ForeignKey(
        "materials.Material",
        on_delete=models.CASCADE,
        related_name="usage_logs",
        verbose_name=_("Материал"),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="material_usage_logs",
        verbose_name=_("Пользователь"),
        blank=True,
        null=True,
    )

    action = models.CharField(
        _("Действие"),
        max_length=MATERIAL_USAGE_ACTION_MAX_LENGTH,
        choices=ActionChoices.choices,
    )
    context = models.CharField(
        _("Контекст"),
        max_length=MATERIAL_USAGE_CONTEXT_MAX_LENGTH,
        choices=ContextChoices.choices,
        default=ContextChoices.LIBRARY,
    )
    context_object_id = models.PositiveBigIntegerField(
        _("ID объекта контекста"),
        blank=True,
        null=True,
    )

    ip_address = models.CharField(
        _("IP-адрес"),
        max_length=MATERIAL_USAGE_IP_ADDRESS_MAX_LENGTH,
        blank=True,
    )
    user_agent = models.CharField(
        _("User-Agent"),
        max_length=MATERIAL_USAGE_USER_AGENT_MAX_LENGTH,
        blank=True,
    )
    metadata = models.JSONField(
        _("Дополнительные данные"),
        default=dict,
        blank=True,
    )

    created_at = models.DateTimeField(
        _("Дата события"),
        auto_now_add=True,
    )

    objects = MaterialUsageLogManager()

    class Meta:
        db_table = "materials_usage_log"
        verbose_name = _("Журнал использования материала")
        verbose_name_plural = _("Журнал использования материалов")
        ordering = (
            "-created_at",
            "-id",
        )
        indexes = [
            models.Index(
                fields=("material",),
                name="mat_usage_material_idx",
            ),
            models.Index(
                fields=("user",),
                name="mat_usage_user_idx",
            ),
            models.Index(
                fields=("action",),
                name="mat_usage_action_idx",
            ),
            models.Index(
                fields=("context",),
                name="mat_usage_context_idx",
            ),
            models.Index(
                fields=("created_at",),
                name="mat_usage_created_idx",
            ),
        ]

    def __str__(self) -> str:
        return f"{self.material} — {self.get_action_display()}"
