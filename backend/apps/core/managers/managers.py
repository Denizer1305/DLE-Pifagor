from __future__ import annotations

from django.db import models

from apps.core.managers.querysets import (
    ArchivableQuerySet,
    LifecycleQuerySet,
    PublishableQuerySet,
    SoftDeleteQuerySet,
    TimeStampedQuerySet,
)


class TimeStampedManager(models.Manager.from_queryset(TimeStampedQuerySet)):
    """
    Менеджер для моделей с created_at и updated_at.
    """


class ArchivableManager(models.Manager.from_queryset(ArchivableQuerySet)):
    """
    Менеджер для моделей с archived_at.
    """


class SoftDeleteManager(models.Manager.from_queryset(SoftDeleteQuerySet)):
    """
    Менеджер для моделей с deleted_at.
    """


class LifecycleManager(models.Manager.from_queryset(LifecycleQuerySet)):
    """
    Менеджер для моделей с archived_at и deleted_at.
    """


class PublishableManager(models.Manager.from_queryset(PublishableQuerySet)):
    """
    Менеджер для моделей с published_at.
    """