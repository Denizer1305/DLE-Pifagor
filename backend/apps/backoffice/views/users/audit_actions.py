from __future__ import annotations

from apps.backoffice.selectors.users import get_backoffice_user_audit_logs_for_actor
from rest_framework.decorators import action
from rest_framework.response import Response


class BackofficeUserAuditActionsMixin:
    """
    Mixin просмотра audit-лога пользователя.
    """

    @action(detail=True, methods=["get"], url_path="audit-logs")
    def audit_logs(self, request, *args, **kwargs):
        """
        Возвращает audit-лог выбранного пользователя.
        """

        target_user = self.get_object()
        audit_logs = get_backoffice_user_audit_logs_for_actor(
            actor=request.user,
            target_user_id=target_user.id,
        )
        serializer = self.get_serializer(audit_logs, many=True)

        return Response(serializer.data)
