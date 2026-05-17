from __future__ import annotations

from apps.users.filters import InviteCodeFilter
from apps.users.models import InviteCode
from apps.users.permissions import CanManageInviteCode, CanViewInviteCodes
from apps.users.serializers import (
    InviteCodeCreatedSerializer,
    InviteCodeCreateSerializer,
    InviteCodeSerializer,
)
from apps.users.services import create_invite_code
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.response import Response


class InviteCodeViewSet(viewsets.ModelViewSet):
    """
    ViewSet кодов приглашения.
    """

    queryset = InviteCode.objects.select_related(
        "organization",
        "department",
        "group",
        "created_by",
        "target_user",
    )
    filterset_class = InviteCodeFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    ordering_fields = [
        "id",
        "expires_at",
        "created_at",
        "updated_at",
    ]
    ordering = [
        "-created_at",
    ]

    def get_serializer_class(self):
        """
        Возвращает serializer.

        Returns:
            Serializer: Класс serializer.
        """

        if self.action == "create":
            return InviteCodeCreateSerializer

        return InviteCodeSerializer

    def get_permissions(self):
        """
        Возвращает permissions.

        Returns:
            list: Permissions.
        """

        if self.action in {"create", "update", "partial_update", "destroy"}:
            return [CanManageInviteCode()]

        return [CanViewInviteCodes()]

    def get_queryset(self):
        """
        Ограничивает список кодов приглашения.

        Returns:
            QuerySet: Коды приглашения.
        """

        user = self.request.user

        if not user.is_authenticated:
            return InviteCode.objects.none()

        if user.is_superuser:
            return self.queryset

        return self.queryset.filter(created_by=user)

    def create(self, request, *args, **kwargs):
        """
        Создаёт код приглашения.

        Пока organization_id, department_id, group_id и target_user_id
        принимаются как IntegerField. После фиксации organizations/
        заменим их на реальные объекты через selectors.

        Args:
            request:
                HTTP-запрос.
            *args:
                Позиционные аргументы.
            **kwargs:
                Именованные аргументы.

        Returns:
            Response: Созданный код и raw_code.
        """

        serializer = InviteCodeCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        invite_code, raw_code = create_invite_code(
            purpose=serializer.validated_data["purpose"],
            created_by=request.user,
            ttl_hours=serializer.validated_data.get("ttl_hours", 72),
            max_uses=serializer.validated_data.get("max_uses", 1),
            request=request,
        )

        response_serializer = InviteCodeCreatedSerializer(
            {
                "invite_code": invite_code,
                "raw_code": raw_code,
            }
        )

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )
