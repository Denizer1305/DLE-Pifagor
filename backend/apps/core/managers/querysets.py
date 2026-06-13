from __future__ import annotations

from django.db import models


class TimeStampedQuerySet(models.QuerySet):
    """
    Базовый QuerySet для моделей с created_at и updated_at.
    """

    def created_after(self, value):
        """
        Возвращает объекты, созданные после указанной даты.
        """

        return self.filter(created_at__gte=value)

    def created_before(self, value):
        """
        Возвращает объекты, созданные до указанной даты.
        """

        return self.filter(created_at__lte=value)

    def updated_after(self, value):
        """
        Возвращает объекты, обновлённые после указанной даты.
        """

        return self.filter(updated_at__gte=value)

    def updated_before(self, value):
        """
        Возвращает объекты, обновлённые до указанной даты.
        """

        return self.filter(updated_at__lte=value)

    def newest(self):
        """
        Сортирует объекты от новых к старым.
        """

        return self.order_by("-created_at", "-id")

    def oldest(self):
        """
        Сортирует объекты от старых к новым.
        """

        return self.order_by("created_at", "id")


class ArchivableQuerySet(TimeStampedQuerySet):
    """
    QuerySet для моделей с archived_at.
    """

    def archived(self):
        """
        Возвращает архивированные объекты.
        """

        return self.filter(archived_at__isnull=False)

    def not_archived(self):
        """
        Возвращает неархивированные объекты.
        """

        return self.filter(archived_at__isnull=True)


class SoftDeleteQuerySet(TimeStampedQuerySet):
    """
    QuerySet для моделей с deleted_at.
    """

    def deleted(self):
        """
        Возвращает мягко удалённые объекты.
        """

        return self.filter(deleted_at__isnull=False)

    def not_deleted(self):
        """
        Возвращает не удалённые мягким удалением объекты.
        """

        return self.filter(deleted_at__isnull=True)


class LifecycleQuerySet(ArchivableQuerySet, SoftDeleteQuerySet):
    """
    QuerySet для моделей с archived_at и deleted_at.
    """

    def active(self):
        """
        Возвращает активные объекты.

        Активный объект — не архивирован и не удалён мягким удалением.
        """

        return self.not_archived().not_deleted()

    def inactive(self):
        """
        Возвращает архивированные или мягко удалённые объекты.
        """

        return self.filter(
            models.Q(archived_at__isnull=False)
            | models.Q(deleted_at__isnull=False)
        )


class PublishableQuerySet(TimeStampedQuerySet):
    """
    QuerySet для моделей с published_at.
    """

    def published(self):
        """
        Возвращает опубликованные объекты.
        """

        return self.filter(published_at__isnull=False)

    def unpublished(self):
        """
        Возвращает неопубликованные объекты.
        """

        return self.filter(published_at__isnull=True)