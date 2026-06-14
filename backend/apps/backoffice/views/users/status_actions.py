from __future__ import annotations

from apps.backoffice.services.users import (
    archive_backoffice_user,
    block_backoffice_user,
    restore_backoffice_user,
    unblock_backoffice_user,
)
from rest_framework.decorators import action


class BackofficeUserStatusActionsMixin:
    """
    Mixin действий изменения статуса пользователя.
    """

    @action(detail=True, methods=["post"], url_path="block")
    def block(self, request, *args, **kwargs):
        """
        Блокирует пользователя.
        """

        target_user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_user = block_backoffice_user(
            actor=request.user,
            target_user=target_user,
            reason=serializer.validated_data.get("reason", ""),
            request=request,
        )

        return self.respond_with_backoffice_user(updated_user)

    @action(detail=True, methods=["post"], url_path="unblock")
    def unblock(self, request, *args, **kwargs):
        """
        Разблокирует пользователя.
        """

        target_user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_user = unblock_backoffice_user(
            actor=request.user,
            target_user=target_user,
            reason=serializer.validated_data.get("reason", ""),
            request=request,
        )

        return self.respond_with_backoffice_user(updated_user)

    @action(detail=True, methods=["post"], url_path="archive")
    def archive(self, request, *args, **kwargs):
        """
        Архивирует пользователя.
        """

        target_user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_user = archive_backoffice_user(
            actor=request.user,
            target_user=target_user,
            reason=serializer.validated_data.get("reason", ""),
            request=request,
        )

        return self.respond_with_backoffice_user(updated_user)

    @action(detail=True, methods=["post"], url_path="restore")
    def restore(self, request, *args, **kwargs):
        """
        Восстанавливает пользователя.
        """

        target_user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_user = restore_backoffice_user(
            actor=request.user,
            target_user=target_user,
            reason=serializer.validated_data.get("reason", ""),
            request=request,
        )

        return self.respond_with_backoffice_user(updated_user)
