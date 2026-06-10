"""
Менеджеры и QuerySet уведомлений.

Здесь собраны часто используемые выборки: активные уведомления, непрочитанные,
прочитанные, истёкшие, уведомления конкретного пользователя и уведомления,
доступные для отображения в интерфейсе.
"""

from __future__ import annotations

from datetime import timedelta

from apps.notifications.constants import NotificationStatus
from django.db import models
from django.utils import timezone


class NotificationQuerySet(models.QuerySet):
    """
    QuerySet уведомлений с доменными фильтрами.
    """

    def for_user(self, user):
        """
        Возвращает уведомления конкретного пользователя.
        """

        return self.filter(recipient=user)

    def unread(self):
        """
        Возвращает непрочитанные уведомления.
        """

        return self.filter(status=NotificationStatus.UNREAD)

    def read(self):
        """
        Возвращает прочитанные уведомления.
        """

        return self.filter(status=NotificationStatus.READ)

    def completed(self):
        """
        Возвращает выполненные уведомления.
        """

        return self.filter(status=NotificationStatus.COMPLETED)

    def archived(self):
        """
        Возвращает архивные уведомления.
        """

        return self.filter(status=NotificationStatus.ARCHIVED)

    def active(self):
        """
        Возвращает уведомления, которые ещё актуальны для интерфейса.
        """

        now = timezone.now()

        return self.exclude(
            status=NotificationStatus.ARCHIVED,
        ).filter(
            models.Q(expires_at__isnull=True) | models.Q(expires_at__gt=now),
        )

    def expired(self):
        """
        Возвращает уведомления, срок хранения которых истёк.
        """

        return self.filter(expires_at__isnull=False, expires_at__lte=timezone.now())

    def visible(self):
        """
        Возвращает уведомления, которые можно показывать пользователю.
        """

        return self.active().exclude(status=NotificationStatus.ARCHIVED)

    def important(self):
        """
        Возвращает важные уведомления.
        """

        return self.filter(level__in=["warning", "danger"])

    def by_level(self, level: str):
        """
        Фильтрует уведомления по уровню важности.
        """

        if not level:
            return self

        return self.filter(level=level)

    def by_type(self, notification_type: str):
        """
        Фильтрует уведомления по типу.
        """

        if not notification_type:
            return self

        return self.filter(notification_type=notification_type)

    def by_category(self, category: str):
        """
        Фильтрует уведомления по категории.
        """

        if not category:
            return self

        return self.filter(category=category)

    def by_status(self, status: str):
        """
        Фильтрует уведомления по статусу.
        """

        if not status:
            return self

        return self.filter(status=status)

    def by_source(self, source_type: str, source_id: str | None = None):
        """
        Фильтрует уведомления по источнику.
        """

        queryset = self

        if source_type:
            queryset = queryset.filter(source_type=source_type)

        if source_id:
            queryset = queryset.filter(source_id=source_id)

        return queryset

    def due_before(self, value):
        """
        Возвращает уведомления, дата события которых раньше указанного времени.
        """

        if value is None:
            return self

        return self.filter(event_at__isnull=False, event_at__lte=value)

    def due_after(self, value):
        """
        Возвращает уведомления, дата события которых позже указанного времени.
        """

        if value is None:
            return self

        return self.filter(event_at__isnull=False, event_at__gte=value)

    def created_today(self):
        """
        Возвращает уведомления, созданные сегодня.
        """

        now = timezone.localtime()
        start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)

        return self.filter(created_at__gte=start, created_at__lt=end)

    def ordered_for_feed(self):
        """
        Сортирует уведомления для ленты пользователя.
        """

        return self.order_by(
            "status",
            "-created_at",
            "-id",
        )

    def latest_first(self):
        """
        Сортирует уведомления от новых к старым.
        """

        return self.order_by("-created_at", "-id")

    def unread_count(self) -> int:
        """
        Возвращает количество непрочитанных уведомлений.
        """

        return self.unread().count()


class NotificationManager(models.Manager.from_queryset(NotificationQuerySet)):
    """
    Менеджер уведомлений.
    """

    def get_queryset(self):
        """
        Возвращает базовый queryset уведомлений.
        """

        return super().get_queryset().select_related("recipient")

    def for_user_feed(self, user):
        """
        Возвращает активную ленту уведомлений пользователя.
        """

        return self.get_queryset().for_user(user).visible().ordered_for_feed()

    def unread_for_user(self, user):
        """
        Возвращает непрочитанные уведомления пользователя.
        """

        return self.get_queryset().for_user(user).visible().unread()

    def unread_count_for_user(self, user) -> int:
        """
        Возвращает количество непрочитанных уведомлений пользователя.
        """

        return self.unread_for_user(user).count()

    def expired_for_cleanup(self):
        """
        Возвращает уведомления для удаления задачей очистки.
        """

        return self.get_queryset().expired()

    def find_by_deduplication_key(self, deduplication_key: str):
        """
        Ищет уведомление по ключу дедупликации.
        """

        if not deduplication_key:
            return None

        return (
            self.get_queryset()
            .filter(
                deduplication_key=deduplication_key,
            )
            .first()
        )

    def exists_by_deduplication_key(self, deduplication_key: str) -> bool:
        """
        Проверяет существование уведомления по ключу дедупликации.
        """

        if not deduplication_key:
            return False

        return (
            self.get_queryset()
            .filter(
                deduplication_key=deduplication_key,
            )
            .exists()
        )
