from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone


class PublishableModel(models.Model):
    """
    Абстрактная модель для сущностей, которые можно публиковать.
    """

    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата публикации",
    )
    published_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Опубликовал",
    )

    class Meta:
        abstract = True

    @property
    def is_published(self) -> bool:
        """
        Проверяет, опубликован ли объект.
        """

        return self.published_at is not None

    def publish(self, *, user=None, save: bool = True) -> None:
        """
        Публикует объект.
        """

        self.published_at = timezone.now()
        self.published_by = user

        if save:
            self.save(update_fields=["published_at", "published_by"])

    def unpublish(self, *, save: bool = True) -> None:
        """
        Снимает объект с публикации.
        """

        self.published_at = None
        self.published_by = None

        if save:
            self.save(update_fields=["published_at", "published_by"])
