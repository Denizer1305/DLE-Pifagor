from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone

from apps.core.models.timestamped import TimeStampedModel


class ArchivableModel(models.Model):
    """
    Абстрактная модель для сущностей, которые можно архивировать.
    """

    archived_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата архивации",
    )
    archived_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Архивировал",
    )
    archive_reason = models.TextField(
        blank=True,
        verbose_name="Причина архивации",
    )

    class Meta:
        abstract = True

    @property
    def is_archived(self) -> bool:
        """
        Проверяет, находится ли объект в архиве.
        """

        return self.archived_at is not None

    def archive(self, *, user=None, reason: str = "", save: bool = True) -> None:
        """
        Архивирует объект.
        """

        self.archived_at = timezone.now()
        self.archived_by = user
        self.archive_reason = reason or ""

        if save:
            self.save(
                update_fields=[
                    "archived_at",
                    "archived_by",
                    "archive_reason",
                ]
            )

    def restore(self, *, save: bool = True) -> None:
        """
        Восстанавливает объект из архива.
        """

        self.archived_at = None
        self.archived_by = None
        self.archive_reason = ""

        if save:
            self.save(
                update_fields=[
                    "archived_at",
                    "archived_by",
                    "archive_reason",
                ]
            )


class SoftDeleteModel(models.Model):
    """
    Абстрактная модель для мягкого удаления.
    """

    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Дата удаления",
    )
    deleted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="+",
        verbose_name="Удалил",
    )
    delete_reason = models.TextField(
        blank=True,
        verbose_name="Причина удаления",
    )

    class Meta:
        abstract = True

    @property
    def is_deleted(self) -> bool:
        """
        Проверяет, удалён ли объект мягким удалением.
        """

        return self.deleted_at is not None

    def soft_delete(
        self,
        *,
        user=None,
        reason: str = "",
        save: bool = True,
    ) -> None:
        """
        Выполняет мягкое удаление объекта.
        """

        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.delete_reason = reason or ""

        if save:
            self.save(
                update_fields=[
                    "deleted_at",
                    "deleted_by",
                    "delete_reason",
                ]
            )

    def restore_deleted(self, *, save: bool = True) -> None:
        """
        Восстанавливает объект после мягкого удаления.
        """

        self.deleted_at = None
        self.deleted_by = None
        self.delete_reason = ""

        if save:
            self.save(
                update_fields=[
                    "deleted_at",
                    "deleted_by",
                    "delete_reason",
                ]
            )


class LifecycleModel(TimeStampedModel, ArchivableModel, SoftDeleteModel):
    """
    Абстрактная модель с базовым жизненным циклом.

    Объединяет:
    - даты создания и обновления;
    - архивацию;
    - мягкое удаление.
    """

    class Meta:
        abstract = True