from __future__ import annotations

from apps.materials.models import MaterialUsageLog
from django.db.models import Q, QuerySet


def material_usage_log_base_queryset() -> QuerySet[MaterialUsageLog]:
    """
    Возвращает базовый queryset журнала использования материалов.
    """

    return MaterialUsageLog.objects.select_related(
        "material",
        "user",
    )


def material_usage_log_list_queryset(
    *,
    search: str | None = None,
    material_id: int | None = None,
    user_id: int | None = None,
    action: str | None = None,
    context: str | None = None,
) -> QuerySet[MaterialUsageLog]:
    """
    Возвращает список событий использования материалов.
    """

    queryset = material_usage_log_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(material__title__icontains=search)
            | Q(material__slug__icontains=search)
            | Q(user__email__icontains=search)
            | Q(user__first_name__icontains=search)
            | Q(user__last_name__icontains=search)
            | Q(ip_address__icontains=search)
            | Q(user_agent__icontains=search)
        )

    if material_id:
        queryset = queryset.filter(material_id=material_id)

    if user_id:
        queryset = queryset.filter(user_id=user_id)

    if action:
        queryset = queryset.filter(action=action)

    if context:
        queryset = queryset.filter(context=context)

    return queryset.order_by(
        "-created_at",
        "-id",
    )


def get_material_usage_log_by_id(
    usage_log_id: int,
) -> MaterialUsageLog:
    """
    Возвращает событие журнала использования материала по идентификатору.
    """

    return material_usage_log_base_queryset().get(id=usage_log_id)


def get_recent_material_usage_logs(
    *,
    material_id: int | None = None,
    limit: int = 50,
) -> QuerySet[MaterialUsageLog]:
    """
    Возвращает последние события использования материалов.
    """

    queryset = material_usage_log_list_queryset(material_id=material_id)

    return queryset[:limit]
