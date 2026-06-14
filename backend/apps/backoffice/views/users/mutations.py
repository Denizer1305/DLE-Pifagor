from __future__ import annotations

from apps.backoffice.services.users import (
    schedule_backoffice_user_deletion,
    update_backoffice_user,
)
from rest_framework import status


class BackofficeUserMutationActionsMixin:
    """
    Mixin базовых mutation-действий пользователя.
    """

    def update(self, request, *args, **kwargs):
        """
        Обновляет пользователя через backoffice.
        """

        target_user = self.get_object()
        serializer = self.get_serializer(
            data=request.data,
            partial=kwargs.get("partial", False),
        )
        serializer.is_valid(raise_exception=True)

        updated_user = update_backoffice_user(
            actor=request.user,
            target_user=target_user,
            data=serializer.get_service_payload(),
            expected_updated_at=serializer.validated_data.get("expected_updated_at"),
            reason=serializer.validated_data.get("reason", ""),
            request=request,
        )

        return self.respond_with_backoffice_user(updated_user)

    def partial_update(self, request, *args, **kwargs):
        """
        Частично обновляет пользователя через backoffice.
        """

        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Планирует удаление пользователя.
        """

        target_user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_user = schedule_backoffice_user_deletion(
            actor=request.user,
            target_user=target_user,
            reason=serializer.validated_data.get("reason", ""),
            scheduled_for_deletion_at=serializer.validated_data.get(
                "scheduled_for_deletion_at"
            ),
            request=request,
        )

        return self.respond_with_backoffice_user(
            updated_user,
            status_code=status.HTTP_202_ACCEPTED,
        )
