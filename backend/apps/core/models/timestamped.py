from __future__ import annotations

from django.db import models


class TimeStampedModel(models.Model):
    """
    Абстрактная модель с датами создания и обновления.

    Используется для большинства сущностей проекта, чтобы везде
    была единая информация о времени создания и последнего изменения.
    """

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата обновления",
    )

    class Meta:
        abstract = True