from __future__ import annotations

from django.db.models import Q, QuerySet


def filter_departments_queryset(
    *,
    queryset: QuerySet,
    params,
) -> QuerySet:
    """
    Фильтрует QuerySet отделений по query params.
    """

    search = (params.get("search") or "").strip()
    organization_id = params.get("organization_id")
    is_active = params.get("is_active")

    if search:
        queryset = queryset.filter(
            Q(name__icontains=search)
            | Q(short_name__icontains=search)
            | Q(code__icontains=search)
            | Q(organization__name__icontains=search)
            | Q(organization__short_name__icontains=search)
        )

    if organization_id:
        queryset = queryset.filter(organization_id=organization_id)

    if is_active in {"true", "false"}:
        queryset = queryset.filter(is_active=is_active == "true")

    return queryset.distinct()
