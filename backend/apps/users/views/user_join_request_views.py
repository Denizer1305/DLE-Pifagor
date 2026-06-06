from __future__ import annotations

from apps.users.filters import UserJoinRequestFilter
from apps.users.models import UserJoinRequest
from apps.users.permissions import IsActiveUser, IsOrganizationReviewerRole
from apps.users.selectors import (
    actor_can_review_join_request,
    get_join_requests_queryset_for_actor,
    get_reviewable_join_requests_queryset_for_actor,
)
from apps.users.serializers import (
    JoinRequestReviewSerializer,
    UserJoinRequestSerializer,
)
from apps.users.services import approve_join_request, reject_join_request
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


class UserJoinRequestViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet заявок пользователей.

    Доступ:
        - обычный пользователь видит свои заявки;
        - целевой пользователь видит связанные с ним заявки;
        - проверяющий видит заявки в своей области;
        - суперадминистратор видит все заявки.

    Действия approve/reject доступны только проверяющим.
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
        Возвращает permissions для действия.

        Returns:
            list: Permissions.
        """

        if self.action in {"approve", "reject"}:
            return [IsOrganizationReviewerRole()]

        return [IsActiveUser()]

    def get_queryset(self):
        """
        Возвращает заявки с учётом текущего пользователя и действия.

        Для approve/reject отдаём только заявки, которые пользователь
        потенциально может рассматривать.

        Returns:
            QuerySet: Доступные заявки.
        """

        actor = self.request.user

        if self.action in {"approve", "reject"}:
            return get_reviewable_join_requests_queryset_for_actor(
                actor=actor,
            )

        return get_join_requests_queryset_for_actor(
            actor=actor,
        )

    def get_serializer_context(self) -> dict:
        """
        Возвращает контекст сериализатора.

        Returns:
            dict: Контекст сериализатора.
        """

        context = super().get_serializer_context()
        context["request"] = self.request

        return context

    @action(
        detail=True,
        methods=["post"],
    )
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

        if not actor_can_review_join_request(
            actor=request.user,
            join_request=join_request,
        ):
            raise PermissionDenied(
                "У пользователя нет прав подтвердить эту заявку."
            )

        serializer = JoinRequestReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        join_request = approve_join_request(
            join_request=join_request,
            reviewer=request.user,
            comment=serializer.validated_data.get("comment", ""),
            request=request,
        )

        output_serializer = UserJoinRequestSerializer(
            join_request,
            context=self.get_serializer_context(),
        )

        return Response(output_serializer.data)

    @action(
        detail=True,
        methods=["post"],
    )
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

        if not actor_can_review_join_request(
            actor=request.user,
            join_request=join_request,
        ):
            raise PermissionDenied(
                "У пользователя нет прав отклонить эту заявку."
            )

        serializer = JoinRequestReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        join_request = reject_join_request(
            join_request=join_request,
            reviewer=request.user,
            comment=serializer.validated_data.get("comment", ""),
            request=request,
        )

        output_serializer = UserJoinRequestSerializer(
            join_request,
            context=self.get_serializer_context(),
        )

        return Response(output_serializer.data)