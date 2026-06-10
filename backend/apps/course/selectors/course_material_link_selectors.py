from __future__ import annotations

from apps.course.models import CourseMaterialLink
from django.db.models import Q, QuerySet


def course_material_link_base_queryset() -> QuerySet[CourseMaterialLink]:
    """
    Возвращает базовый queryset связей курса с материалами.
    """

    return CourseMaterialLink.objects.select_related(
        "course",
        "section",
        "lesson",
        "material",
        "course__owner_teacher",
        "course__organization",
    )


def course_material_link_list_queryset(
    *,
    search: str | None = None,
    course_id: int | None = None,
    section_id: int | None = None,
    lesson_id: int | None = None,
    material_id: int | None = None,
    placement: str | None = None,
    is_required: bool | None = None,
    is_visible: bool | None = None,
) -> QuerySet[CourseMaterialLink]:
    """
    Возвращает список связей курса с материалами.
    """

    queryset = course_material_link_base_queryset()

    if search:
        queryset = queryset.filter(
            Q(course__title__icontains=search)
            | Q(course__code__icontains=search)
            | Q(section__title__icontains=search)
            | Q(lesson__title__icontains=search)
            | Q(material__title__icontains=search)
            | Q(material__slug__icontains=search)
            | Q(notes__icontains=search)
        )

    if course_id:
        queryset = queryset.filter(course_id=course_id)

    if section_id:
        queryset = queryset.filter(section_id=section_id)

    if lesson_id:
        queryset = queryset.filter(lesson_id=lesson_id)

    if material_id:
        queryset = queryset.filter(material_id=material_id)

    if placement:
        queryset = queryset.filter(placement=placement)

    if is_required is not None:
        queryset = queryset.filter(is_required=is_required)

    if is_visible is not None:
        queryset = queryset.filter(is_visible=is_visible)

    return queryset.order_by(
        "course_id",
        "section__order",
        "lesson__order",
        "order",
        "id",
    )


def course_material_link_detail_queryset() -> QuerySet[CourseMaterialLink]:
    """
    Возвращает queryset связи курса с материалом.
    """

    return course_material_link_base_queryset()


def get_course_material_link_by_id(
    link_id: int,
) -> CourseMaterialLink:
    """
    Возвращает связь курса с материалом по идентификатору.
    """

    return course_material_link_detail_queryset().get(id=link_id)
