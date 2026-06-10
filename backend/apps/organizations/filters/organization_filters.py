from __future__ import annotations

from django.db.models import Q, QuerySet


def filter_organizations_queryset(
    *,
    queryset: QuerySet,
    params,
) -> QuerySet:
    """
    Фильтрует QuerySet организаций по query params.
    """

    search = (params.get("search") or "").strip()
    city = (params.get("city") or "").strip()
    is_active = params.get("is_active")
    is_public = params.get("is_public")

    if search:
        queryset = queryset.filter(
            Q(name__icontains=search)
            | Q(short_name__icontains=search)
            | Q(code__icontains=search)
            | Q(city__icontains=search)
            | Q(email__icontains=search)
        )

    if city:
        queryset = queryset.filter(city__icontains=city)

    if is_active in {"true", "false"}:
        queryset = queryset.filter(is_active=is_active == "true")

    if is_public in {"true", "false"}:
        queryset = queryset.filter(is_public=is_public == "true")

    return queryset.distinct()
