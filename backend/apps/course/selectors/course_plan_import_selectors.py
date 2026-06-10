from __future__ import annotations

from apps.course.models import CoursePlanImport
from django.db.models import Q, QuerySet


def course_plan_import_base_queryset() -> QuerySet[CoursePlanImport]:
    """
    Возвращает базовый queryset импортов КТП.
    """

    return CoursePlanImport.objects.select_related(
        "course_plan",
        "course_plan__course",
        "imported_by",
    )


def course_plan_import_list_queryset(
    *,
    search: str | None = None,
    course_plan_id: int | None = None,
    status: str | None = None,
    imported_by_id: int | None = None,
) -> QuerySet[CoursePlanImport]:
    """
    Возвращает список импортов КТП.
    """

    queryset = course_plan_import_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(course_plan__course__title__icontains=search)
            | Q(original_filename__icontains=search)
            | Q(file_hash__icontains=search)
            | Q(parser_version__icontains=search)
            | Q(imported_by__email__icontains=search)
            | Q(imported_by__first_name__icontains=search)
            | Q(imported_by__last_name__icontains=search)
        )

    if course_plan_id:
        queryset = queryset.filter(course_plan_id=course_plan_id)

    if status:
        queryset = queryset.filter(status=status)

    if imported_by_id:
        queryset = queryset.filter(imported_by_id=imported_by_id)

    return queryset.order_by(
        "-imported_at",
        "-id",
    )


def course_plan_import_detail_queryset() -> QuerySet[CoursePlanImport]:
    """
    Возвращает queryset импорта КТП с деталями.
    """

    return course_plan_import_base_queryset()


def get_course_plan_import_by_id(
    import_id: int,
) -> CoursePlanImport:
    """
    Возвращает импорт КТП по идентификатору.
    """

    return course_plan_import_detail_queryset().get(id=import_id)
