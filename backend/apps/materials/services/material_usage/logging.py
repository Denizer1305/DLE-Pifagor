from __future__ import annotations

from typing import Any

from apps.materials.models import Material, MaterialUsageLog
from django.db import transaction


@transaction.atomic
def log_material_usage(
    *,
    material: Material,
    action: str,
    context: str = MaterialUsageLog.ContextChoices.LIBRARY,
    user=None,
    context_object_id: int | None = None,
    request=None,
    metadata: dict[str, Any] | None = None,
) -> MaterialUsageLog:
    """
    Создаёт запись журнала использования материала.
    """

    ip_address = ""
    user_agent = ""

    if request is not None:
        ip_address = _get_client_ip(request)
        user_agent = request.META.get("HTTP_USER_AGENT", "")[:512]

        if user is None and getattr(request, "user", None):
            user = request.user

    if user is not None and not getattr(user, "is_authenticated", False):
        user = None

    usage_log = MaterialUsageLog.objects.create(
        material=material,
        user=user,
        action=action,
        context=context,
        context_object_id=context_object_id,
        ip_address=ip_address,
        user_agent=user_agent,
        metadata=metadata or {},
    )

    return usage_log


def _get_client_ip(request) -> str:
    """
    Возвращает IP-адрес клиента из request.
    """

    forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")

    if forwarded_for:
        return forwarded_for.split(",")[0].strip()[:64]

    return request.META.get("REMOTE_ADDR", "")[:64]
