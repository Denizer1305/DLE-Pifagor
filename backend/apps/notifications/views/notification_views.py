"""
API представления уведомлений.

ViewSet отвечает за:
- bootstrap-синхронизацию уведомлений;
- получение ленты уведомлений пользователя;
- получение счётчика непрочитанных уведомлений;
- отметку уведомления как прочитанного;
- массовую отметку всех уведомлений как прочитанных;
- выполнение уведомления;
- удаление уведомления.
"""

from __future__ import annotations

from apps.notifications.filters import apply_notification_filters
from apps.notifications.permissions import CanAccessNotifications
from apps.notifications.selectors import (
    get_user_notification_by_id,
    get_user_notifications_queryset,
    get_user_unread_notifications_count,
)
from apps.notifications.serializers import (
    NotificationActionResponseSerializer,
    NotificationBootstrapRequestSerializer,
    NotificationBootstrapResponseSerializer,
    NotificationBulkActionResponseSerializer,
    NotificationDeleteResponseSerializer,
    NotificationDetailSerializer,
    NotificationFeedSerializer,
    NotificationListSerializer,
    NotificationQuerySerializer,
    NotificationUnreadCountSerializer,
)
from apps.notifications.services import (
    bootstrap_notifications_for_user,
    complete_notification,
    delete_notification,
    mark_all_notifications_as_read,
    mark_notification_as_read,
)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class NotificationViewSet(viewsets.ViewSet):
    """
    ViewSet внутренних уведомлений пользователя.
    """

    permission_classes = [
        CanAccessNotifications,
    ]

    def list(self, request):
        """
        Возвращает ленту уведомлений текущего пользователя.

        Поддерживает фильтрацию через query-параметры:
        status, level, category, notification_type, source_type, source_id,
        unread_only.
        """

        query_serializer = NotificationQuerySerializer(data=request.query_params)
        query_serializer.is_valid(raise_exception=True)

        queryset = get_user_notifications_queryset(request.user)
        queryset = apply_notification_filters(
            queryset=queryset,
            filters=query_serializer.validated_data,
        )

        serializer = NotificationFeedSerializer(
            {
                "unread_count": get_user_unread_notifications_count(request.user),
                "items": NotificationListSerializer(queryset, many=True).data,
            }
        )

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        """
        Возвращает детальную информацию об уведомлении пользователя.
        """

        notification = get_user_notification_by_id(
            user=request.user,
            notification_id=pk,
        )

        return Response(
            NotificationDetailSerializer(notification).data,
            status=status.HTTP_200_OK,
        )

    def destroy(self, request, pk=None):
        """
        Удаляет уведомление пользователя.
        """

        delete_notification(
            user=request.user,
            notification_id=pk,
        )

        payload = {
            "detail": "Уведомление удалено.",
        }

        return Response(
            NotificationDeleteResponseSerializer(payload).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=[
            "post",
        ],
        url_path="bootstrap",
    )
    def bootstrap(self, request):
        """
        Синхронизирует уведомления пользователя на текущий день.

        Используется frontend частью при входе пользователя в личный кабинет.
        Основная генерация идёт через Celery, а bootstrap догенерирует
        недостающие уведомления без дублей.
        """

        serializer = NotificationBootstrapRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        payload = bootstrap_notifications_for_user(
            user=request.user,
            target_date=serializer.validated_data.get("target_date"),
        )
        payload["unread_count"] = get_user_unread_notifications_count(request.user)

        return Response(
            NotificationBootstrapResponseSerializer(payload).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=[
            "get",
        ],
        url_path="me",
    )
    def me(self, request):
        """
        Возвращает ленту уведомлений текущего пользователя.

        Дублирует list endpoint в более явном формате:
        /api/v1/notifications/me/
        """

        return self.list(request)

    @action(
        detail=False,
        methods=[
            "get",
        ],
        url_path="me/unread-count",
    )
    def unread_count(self, request):
        """
        Возвращает количество непрочитанных уведомлений пользователя.
        """

        payload = {
            "unread_count": get_user_unread_notifications_count(request.user),
        }

        return Response(
            NotificationUnreadCountSerializer(payload).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=[
            "post",
        ],
        url_path="read",
    )
    def read(self, request, pk=None):
        """
        Отмечает уведомление как прочитанное.
        """

        notification = mark_notification_as_read(
            user=request.user,
            notification_id=pk,
        )

        payload = {
            "detail": "Уведомление отмечено как прочитанное.",
            "notification": notification,
        }

        return Response(
            NotificationActionResponseSerializer(payload).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=[
            "post",
        ],
        url_path="read-all",
    )
    def read_all(self, request):
        """
        Отмечает все уведомления пользователя как прочитанные.
        """

        updated_count = mark_all_notifications_as_read(user=request.user)

        payload = {
            "detail": "Все уведомления отмечены как прочитанные.",
            "updated_count": updated_count,
            "unread_count": get_user_unread_notifications_count(request.user),
        }

        return Response(
            NotificationBulkActionResponseSerializer(payload).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=[
            "post",
        ],
        url_path="complete",
    )
    def complete(self, request, pk=None):
        """
        Отмечает уведомление как выполненное.
        """

        notification = complete_notification(
            user=request.user,
            notification_id=pk,
        )

        payload = {
            "detail": "Уведомление отмечено как выполненное.",
            "notification": notification,
        }

        return Response(
            NotificationActionResponseSerializer(payload).data,
            status=status.HTTP_200_OK,
        )
