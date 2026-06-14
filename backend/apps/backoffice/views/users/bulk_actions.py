from __future__ import annotations

from apps.backoffice.serializers.users import BackofficeUserBulkResultSerializer
from apps.backoffice.services.users import execute_backoffice_users_bulk_action
from rest_framework.decorators import action
from rest_framework.response import Response


class BackofficeUserBulkActionsMixin:
    """
    Mixin массовых действий над пользователями.
    """

    @action(detail=False, methods=["post"], url_path="bulk")
    def bulk(self, request, *args, **kwargs):
        """
        Выполняет массовое действие над пользователями.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = execute_backoffice_users_bulk_action(
            actor=request.user,
            action=serializer.validated_data["action"],
            user_ids=serializer.validated_data["user_ids"],
            reason=serializer.validated_data.get("reason", ""),
            role_payload=serializer.validated_data.get("role_payload"),
            expected_updated_at_map=serializer.validated_data.get(
                "expected_updated_at_map"
            ),
            request=request,
        )

        result_serializer = BackofficeUserBulkResultSerializer(result.as_dict())

        return Response(result_serializer.data)
