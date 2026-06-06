from __future__ import annotations

from django.db.models import Q, QuerySet


def filter_subjects_queryset(
    *,
    queryset: QuerySet,
    params,
) -> QuerySet:
    """
    Фильтрует QuerySet учебных предметов по query params.

    Args:
        queryset:
            Исходный QuerySet предметов.
        params:
            Query params из request.

    Returns:
        QuerySet: Отфильтрованные предметы.
    """

    search = (params.get("search") or "").strip()
    is_active = params.get("is_active")

    if search:
        queryset = queryset.filter(
            Q(name__icontains=search)
            | Q(short_name__icontains=search)
            | Q(code__icontains=search)
            | Q(description__icontains=search)
        )

    if is_active in {"true", "false"}:
        queryset = queryset.filter(
            is_active=is_active == "true",
        )

    return queryset.distinct()