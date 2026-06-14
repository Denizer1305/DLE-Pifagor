from __future__ import annotations

from apps.backoffice.selectors.users import get_backoffice_roles_queryset
from apps.backoffice.services.users import change_backoffice_user_roles
from rest_framework.decorators import action
from rest_framework.response import Response


class BackofficeUserRoleActionsMixin:
    """
    Mixin действий управления ролями пользователя.
    """

    @action(detail=True, methods=["post"], url_path="change-roles")
    def change_roles(self, request, *args, **kwargs):
        """
        Изменяет роли пользователя.
        """

        target_user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        change_backoffice_user_roles(
            actor=request.user,
            target_user=target_user,
            assigned_roles=serializer.validated_data.get("assigned_roles") or [],
            revoked_user_role_ids=(
                serializer.validated_data.get("revoked_user_role_ids") or []
            ),
            reason=serializer.validated_data.get("reason", ""),
            request=request,
        )

        return self.respond_with_backoffice_user(target_user)

    @action(detail=False, methods=["get"], url_path="available-roles")
    def available_roles(self, request, *args, **kwargs):
        """
        Возвращает роли, доступные для выбора в backoffice.
        """

        roles = get_backoffice_roles_queryset()
        serializer = self.get_serializer(roles, many=True)

        return Response(serializer.data)
