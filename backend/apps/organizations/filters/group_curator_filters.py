from __future__ import annotations

from django.db.models import Q, QuerySet


def filter_group_curators_queryset(
    *,
    queryset: QuerySet,
    params,
) -> QuerySet:
    """
    Фильтрует кураторов групп.
    """

    search = (params.get("search") or "").strip()
    organization_id = params.get("organization_id")
    department_id = params.get("department_id")
    group_id = params.get("group_id")
    is_active = params.get("is_active")
    is_primary = params.get("is_primary")

    if search:
        queryset = queryset.filter(
            Q(teacher__email__icontains=search)
            | Q(teacher__first_name__icontains=search)
            | Q(teacher__last_name__icontains=search)
            | Q(group__name__icontains=search)
            | Q(group__code__icontains=search)
        )

    if organization_id:
        queryset = queryset.filter(group__organization_id=organization_id)

    if department_id:
        queryset = queryset.filter(group__department_id=department_id)

    if group_id:
        queryset = queryset.filter(group_id=group_id)

    if is_active in {"true", "false"}:
        queryset = queryset.filter(is_active=is_active == "true")

    if is_primary in {"true", "false"}:
        queryset = queryset.filter(is_primary=is_primary == "true")

    return queryset.distinct()
