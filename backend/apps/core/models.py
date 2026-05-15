from django.conf import settings
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """
    Абстрактная модель с датами создания и обновления.

    Используется для большинства сущностей проекта, чтобы везде
    была единая информация о времени создания и последнего изменения.

    Поля:
        created_at:
            Дата и время создания объекта.
        updated_at:
            Дата и время последнего обновления объекта.
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


class CreatedByModel(models.Model):
    """
    Абстрактная модель с информацией о пользователе, создавшем объект.

    Используется для сущностей, где важно понимать автора:
    задания, уроки, материалы, заявки, коды приглашения и т.д.

    Поля:
        created_by:
            Пользователь, создавший объект.
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

    Поля:
        updated_by:
            Пользователь, который последним изменил объект.
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

    Удобна для административных и важных доменных сущностей,
    где нужно знать, кто создал и кто изменил объект.
    """

    class Meta:
        abstract = True


class ArchivableModel(models.Model):
    """
    Абстрактная модель для сущностей, которые можно архивировать.

    Архивация используется вместо физического удаления, когда объект
    должен исчезнуть из активной работы, но его история ещё важна.

    Поля:
        archived_at:
            Дата и время архивации.
        archived_by:
            Пользователь, который выполнил архивацию.
        archive_reason:
            Причина архивации.
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

        Returns:
            bool: True, если объект архивирован, иначе False.
        """

        return self.archived_at is not None

    def archive(self, *, user=None, reason: str = "", save: bool = True) -> None:
        """
        Архивирует объект.

        Args:
            user:
                Пользователь, который выполняет архивацию.
            reason:
                Причина архивации.
            save:
                Нужно ли сразу сохранять объект в БД.
        """

        self.archived_at = timezone.now()
        self.archived_by = user
        self.archive_reason = reason or ""

        if save:
            self.save(update_fields=["archived_at", "archived_by", "archive_reason"])

    def restore(self, *, save: bool = True) -> None:
        """
        Восстанавливает объект из архива.

        Args:
            save:
                Нужно ли сразу сохранять объект в БД.
        """

        self.archived_at = None
        self.archived_by = None
        self.archive_reason = ""

        if save:
            self.save(update_fields=["archived_at", "archived_by", "archive_reason"])


class SoftDeleteModel(models.Model):
    """
    Абстрактная модель для мягкого удаления.

    Мягкое удаление используется там, где объект не должен сразу
    физически удаляться из базы данных.

    Поля:
        deleted_at:
            Дата и время мягкого удаления.
        deleted_by:
            Пользователь, который выполнил удаление.
        delete_reason:
            Причина удаления.
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

        Returns:
            bool: True, если объект мягко удалён, иначе False.
        """

        return self.deleted_at is not None

    def soft_delete(self, *, user=None, reason: str = "", save: bool = True) -> None:
        """
        Выполняет мягкое удаление объекта.

        Args:
            user:
                Пользователь, который выполняет удаление.
            reason:
                Причина удаления.
            save:
                Нужно ли сразу сохранять объект в БД.
        """

        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.delete_reason = reason or ""

        if save:
            self.save(update_fields=["deleted_at", "deleted_by", "delete_reason"])

    def restore_deleted(self, *, save: bool = True) -> None:
        """
        Восстанавливает объект после мягкого удаления.

        Args:
            save:
                Нужно ли сразу сохранять объект в БД.
        """

        self.deleted_at = None
        self.deleted_by = None
        self.delete_reason = ""

        if save:
            self.save(update_fields=["deleted_at", "deleted_by", "delete_reason"])


class LifecycleModel(TimeStampedModel, ArchivableModel, SoftDeleteModel):
    """
    Абстрактная модель с базовым жизненным циклом.

    Объединяет:
        - даты создания и обновления;
        - архивацию;
        - мягкое удаление.

    Подходит для сущностей, которые нельзя просто удалять из базы:
    пользователей, заявок, материалов, курсов, заданий и т.д.
    """

    class Meta:
        abstract = True


class PublishableModel(models.Model):
    """
    Абстрактная модель для сущностей, которые можно публиковать.

    Подходит для уроков, курсов, материалов, объявлений,
    олимпиад и других объектов с черновиком и публикацией.

    Поля:
        published_at:
            Дата и время публикации.
        published_by:
            Пользователь, который опубликовал объект.
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

        Returns:
            bool: True, если объект опубликован, иначе False.
        """

        return self.published_at is not None

    def publish(self, *, user=None, save: bool = True) -> None:
        """
        Публикует объект.

        Args:
            user:
                Пользователь, который публикует объект.
            save:
                Нужно ли сразу сохранять объект в БД.
        """

        self.published_at = timezone.now()
        self.published_by = user

        if save:
            self.save(update_fields=["published_at", "published_by"])

    def unpublish(self, *, save: bool = True) -> None:
        """
        Снимает объект с публикации.

        Args:
            save:
                Нужно ли сразу сохранять объект в БД.
        """

        self.published_at = None
        self.published_by = None

        if save:
            self.save(update_fields=["published_at", "published_by"])
