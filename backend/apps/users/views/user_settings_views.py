from __future__ import annotations

from apps.users.models import UserSettings
from apps.users.permissions import IsActiveUser
from apps.users.serializers import (
    SetActiveRoleSerializer,
    UserSettingsSerializer,
    UserSettingsUpdateSerializer,
)
from apps.users.services import create_default_user_settings, set_active_role
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class UserSettingsViewSet(viewsets.ModelViewSet):
    """
    ViewSet настроек пользователя.
    """

    serializer_class = UserSettingsSerializer
    permission_classes = [IsActiveUser]

    def get_queryset(self):
        """
        Возвращает настройки текущего пользователя.

        Returns:
            QuerySet: Настройки пользователя.
        """

        user = self.request.user

        if not user.is_authenticated:
            return UserSettings.objects.none()

        return UserSettings.objects.filter(user=user)

    def get_serializer_class(self):
        """
        Возвращает serializer.

        Returns:
            Serializer: Класс serializer.
        """

        if self.action in {"update", "partial_update"}:
            return UserSettingsUpdateSerializer

        if self.action == "set_active_role":
            return SetActiveRoleSerializer

        return UserSettingsSerializer

    @action(detail=False, methods=["get"])
    def me(self, request):
        """
        Возвращает настройки текущего пользователя.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Настройки пользователя.
        """

        settings = create_default_user_settings(user=request.user)

        return Response(
            UserSettingsSerializer(settings).data,
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], url_path="set-active-role")
    def set_active_role(self, request):
        """
        Устанавливает активную роль пользователя.

        Args:
            request:
                HTTP-запрос.

        Returns:
            Response: Обновлённые настройки.
        """

        serializer = SetActiveRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        settings = set_active_role(
            user=request.user,
            role_code=serializer.validated_data["role_code"],
        )

        return Response(UserSettingsSerializer(settings).data)
