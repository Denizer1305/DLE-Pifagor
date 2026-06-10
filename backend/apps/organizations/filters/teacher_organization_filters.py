from __future__ import annotations

from django.db.models import Q, QuerySet


def filter_teacher_organizations_queryset(
    *,
    queryset: QuerySet,
    params,
) -> QuerySet:
    """
    Фильтрует связи преподавателей с организациями.
    """

    search = (params.get("search") or "").strip()
    organization_id = params.get("organization_id")
    employment_type = (params.get("employment_type") or "").strip()
    is_active = params.get("is_active")
    is_primary = params.get("is_primary")

    if search:
        queryset = queryset.filter(
            Q(teacher__email__icontains=search)
            | Q(teacher__first_name__icontains=search)
            | Q(teacher__last_name__icontains=search)
            | Q(organization__name__icontains=search)
            | Q(position__icontains=search)
        )

    if organization_id:
        queryset = queryset.filter(organization_id=organization_id)

    if employment_type:
        queryset = queryset.filter(employment_type=employment_type)

    if is_active in {"true", "false"}:
        queryset = queryset.filter(is_active=is_active == "true")

    if is_primary in {"true", "false"}:
        queryset = queryset.filter(is_primary=is_primary == "true")

    return queryset.distinct()
