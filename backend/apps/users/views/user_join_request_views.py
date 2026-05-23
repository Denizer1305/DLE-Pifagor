from __future__ import annotations

from apps.users.filters import UserJoinRequestFilter
from apps.users.models import UserJoinRequest
from apps.users.permissions import IsOrganizationReviewerRole
from apps.users.serializers import (
    JoinRequestReviewSerializer,
    UserJoinRequestSerializer,
)
from apps.users.services import approve_join_request, reject_join_request
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class UserJoinRequestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet заявок пользователей.
    """

    queryset = UserJoinRequest.objects.select_related(
        "user",
        "target_user",
        "organization",
        "department",
        "group",
        "reviewed_by",
    )
    serializer_class = UserJoinRequestSerializer
    filterset_class = UserJoinRequestFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    ordering_fields = [
        "id",
        "created_at",
        "reviewed_at",
        "expires_at",
    ]
    ordering = [
        "-created_at",
    ]

    def get_permissions(self):
        """
        Возвращает permissions.

        Returns:
            list: Permissions.
        """

        if self.action in {"approve", "reject"}:
            return [IsOrganizationReviewerRole()]

        return [IsOrganizationReviewerRole()]

    def get_queryset(self):
        """
        Ограничивает список заявок.

        Returns:
            QuerySet: Заявки.
        """

        user = self.request.user

        if not user.is_authenticated:
            return UserJoinRequest.objects.none()

        if user.is_superuser:
            return self.queryset

        return self.queryset.filter(user=user)

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        """
        Подтверждает заявку.

        Args:
            request:
                HTTP-запрос.
            pk:
                ID заявки.

        Returns:
            Response: Обновлённая заявка.
        """

        join_request = self.get_object()
        serializer = JoinRequestReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        join_request = approve_join_request(
            join_request=join_request,
            reviewer=request.user,
            comment=serializer.validated_data.get("comment", ""),
            request=request,
        )

        return Response(UserJoinRequestSerializer(join_request).data)

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        """
        Отклоняет заявку.

        Args:
            request:
                HTTP-запрос.
            pk:
                ID заявки.

        Returns:
            Response: Обновлённая заявка.
        """

        join_request = self.get_object()
        serializer = JoinRequestReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        join_request = reject_join_request(
            join_request=join_request,
            reviewer=request.user,
            comment=serializer.validated_data.get("comment", ""),
            request=request,
        )

        return Response(UserJoinRequestSerializer(join_request).data)
