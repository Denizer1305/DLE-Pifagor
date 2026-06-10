from __future__ import annotations

from django.db.models import Q, QuerySet


def filter_study_groups_queryset(
    *,
    queryset: QuerySet,
    params,
) -> QuerySet:
    """
    Фильтрует QuerySet учебных групп по query params.
    """

    search = (params.get("search") or "").strip()
    organization_id = params.get("organization_id")
    department_id = params.get("department_id")
    status = (params.get("status") or "").strip()
    study_form = (params.get("study_form") or "").strip()
    course_number = params.get("course_number")
    is_active = params.get("is_active")

    if search:
        queryset = queryset.filter(
            Q(name__icontains=search)
            | Q(code__icontains=search)
            | Q(organization__name__icontains=search)
            | Q(department__name__icontains=search)
        )

    if organization_id:
        queryset = queryset.filter(organization_id=organization_id)

    if department_id:
        queryset = queryset.filter(department_id=department_id)

    if status:
        queryset = queryset.filter(status=status)

    if study_form:
        queryset = queryset.filter(study_form=study_form)

    if course_number:
        queryset = queryset.filter(course_number=course_number)

    if is_active in {"true", "false"}:
        queryset = queryset.filter(is_active=is_active == "true")

    return queryset.distinct()
