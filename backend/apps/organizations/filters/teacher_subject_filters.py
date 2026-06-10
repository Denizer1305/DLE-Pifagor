from __future__ import annotations

from django.db.models import Q, QuerySet


def filter_teacher_subjects_queryset(
    *,
    queryset: QuerySet,
    params,
) -> QuerySet:
    """
    Фильтрует QuerySet предметов преподавателей по query params.

    Args:
        queryset:
            Исходный QuerySet связей преподавателей с предметами.
        params:
            Query params из request.

    Returns:
        QuerySet: Отфильтрованные связи преподавателей с предметами.
    """

    search = (params.get("search") or "").strip()
    subject_id = params.get("subject_id")
    teacher_id = params.get("teacher_id")
    organization_id = params.get("organization_id")
    is_active = params.get("is_active")
    is_primary = params.get("is_primary")

    if search:
        queryset = queryset.filter(
            Q(teacher__email__icontains=search)
            | Q(teacher__phone__icontains=search)
            | Q(teacher__first_name__icontains=search)
            | Q(teacher__last_name__icontains=search)
            | Q(teacher__middle_name__icontains=search)
            | Q(subject__name__icontains=search)
            | Q(subject__short_name__icontains=search)
            | Q(subject__code__icontains=search)
            | Q(notes__icontains=search)
        )

    if subject_id:
        queryset = queryset.filter(
            subject_id=subject_id,
        )

    if teacher_id:
        queryset = queryset.filter(
            teacher_id=teacher_id,
        )

    if organization_id:
        queryset = queryset.filter(
            Q(teacher__teacher_profile__organization_id=organization_id)
            | Q(
                teacher__teacher_organizations__organization_id=organization_id,
                teacher__teacher_organizations__is_active=True,
            )
        )

    if is_active in {"true", "false"}:
        queryset = queryset.filter(
            is_active=is_active == "true",
        )

    if is_primary in {"true", "false"}:
        queryset = queryset.filter(
            is_primary=is_primary == "true",
        )

    return queryset.distinct()
