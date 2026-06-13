from __future__ import annotations

from django.conf import settings
from django.db import models


class CreatedByModel(models.Model):
    """
    Абстрактная модель с информацией о пользователе, создавшем объект.
    """

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Создал",
    )

    class Meta:
        abstract = True


class UpdatedByModel(models.Model):
    """
    Абстрактная модель с информацией о пользователе, изменившем объект.
    """

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Обновил",
    )

    class Meta:
        abstract = True


class AuditFieldsModel(CreatedByModel, UpdatedByModel):
    """
    Абстрактная модель с полями автора создания и автора обновления.
    """

    class Meta:
        abstract = True