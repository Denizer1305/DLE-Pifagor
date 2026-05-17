from __future__ import annotations

from apps.users.filters import UserFilter
from apps.users.models import User
from apps.users.permissions import (
    CanManageUserLifecycle,
    CanUpdateUser,
    CanViewUser,
    IsActiveUser,
)
from apps.users.serializers import UserDetailSerializer, UserUpdateSerializer
from apps.users.services import anonymize_user, archive_user, block_user
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet пользователей.

    Поддерживает:
        - просмотр пользователей;
        - обновление собственных данных;
        - lifecycle-действия для администратора.
    """

    queryset = User.objects.all()
    filterset_class = UserFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = [
        "email",
        "phone",
        "first_name",
        "last_name",
        "middle_name",
    ]
    ordering_fields = [
        "id",
        "email",
        "last_name",
        "first_name",
        "created_at",
        "updated_at",
    ]
    ordering = [
        "last_name",
        "first_name",
    ]

    def get_serializer_class(self):
        """
        Возвращает serializer в зависимости от действия.

        Returns:
            Serializer: Класс serializer.
        """

        if self.action in {"update", "partial_update"}:
            return UserUpdateSerializer

        return UserDetailSerializer

    def get_permissions(self):
        """
        Возвращает permissions в зависимости от действия.

        Returns:
            list: Список permission instances.
        """

        if self.action in {"update", "partial_update"}:
            return [CanUpdateUser()]

        if self.action in {"block", "archive", "anonymize"}:
            return [CanManageUserLifecycle()]

        return [CanViewUser()]

    def get_queryset(self):
        """
        Возвращает QuerySet пользователей.

        Обычный пользователь видит только себя.
        Расширение доступа по организациям позже можно добавить
        после окончательной реализации organizations/.

        Returns:
            QuerySet: Пользователи.
        """

        user = self.request.user

        if not user.is_authenticated:
            return User.objects.none()

        if user.is_superuser:
            return self.queryset

        return self.queryset.filter(id=user.id)

    @action(detail=False, methods=["get"], permission_classes=[IsActiveUser])
    def me(self, request):
        """
        Возвращает текущего пользователя.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Данные текущего пользователя.
        """

        return Response(
            UserDetailSerializer(request.user).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["post"])
    def block(self, request, pk=None):
        """
        Блокирует пользователя.

        Args:
            request:
                HTTP-запрос.
            pk:
                ID пользователя.

        Returns:
            Response: Обновлённый пользователь.
        """

        user = self.get_object()
        user = block_user(
            user=user,
            actor=request.user,
            reason=request.data.get("reason", ""),
            request=request,
        )

        return Response(UserDetailSerializer(user).data)

    @action(detail=True, methods=["post"])
    def archive(self, request, pk=None):
        """
        Архивирует пользователя.

        Args:
            request:
                HTTP-запрос.
            pk:
                ID пользователя.

        Returns:
            Response: Обновлённый пользователь.
        """

        user = self.get_object()
        user = archive_user(
            user=user,
            actor=request.user,
            reason=request.data.get("reason", ""),
            request=request,
        )

        return Response(UserDetailSerializer(user).data)

    @action(detail=True, methods=["post"])
    def anonymize(self, request, pk=None):
        """
        Анонимизирует пользователя.

        Args:
            request:
                HTTP-запрос.
            pk:
                ID пользователя.

        Returns:
            Response: Обновлённый пользователь.
        """

        user = self.get_object()
        user = anonymize_user(
            user=user,
            actor=request.user,
            reason=request.data.get("reason", ""),
            request=request,
        )

        return Response(UserDetailSerializer(user).data)
