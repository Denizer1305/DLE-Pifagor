from __future__ import annotations

from typing import Any

from apps.course.models import CourseMaterialLink
from apps.course.selectors import get_course_material_link_by_id
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _

COURSE_MATERIAL_LINK_MUTABLE_FIELDS = {
    "course",
    "course_id",
    "section",
    "section_id",
    "lesson",
    "lesson_id",
    "material",
    "material_id",
    "placement",
    "order",
    "is_required",
    "is_visible",
    "notes",
}


@transaction.atomic
def create_course_material_link(
    *,
    data: dict[str, Any],
) -> CourseMaterialLink:
    """
    Создаёт связь курса с материалом.
    """

    link = CourseMaterialLink()

    _apply_course_material_link_data(
        link=link,
        data=data,
    )

    validate_course_material_link_can_be_saved(link=link)

    link.full_clean()
    link.save()

    return link


@transaction.atomic
def update_course_material_link(
    *,
    link: CourseMaterialLink,
    data: dict[str, Any],
) -> CourseMaterialLink:
    """
    Обновляет связь курса с материалом.
    """

    _apply_course_material_link_data(
        link=link,
        data=data,
    )

    validate_course_material_link_can_be_saved(link=link)

    link.full_clean()
    link.save()

    return link


@transaction.atomic
def update_course_material_link_by_id(
    *,
    link_id: int,
    data: dict[str, Any],
) -> CourseMaterialLink:
    """
    Обновляет связь курса с материалом по идентификатору.
    """

    link = get_course_material_link_by_id(link_id)

    return update_course_material_link(
        link=link,
        data=data,
    )


@transaction.atomic
def hide_course_material_link(
    *,
    link: CourseMaterialLink,
) -> CourseMaterialLink:
    """
    Скрывает материал курса.
    """

    link.is_visible = False
    link.full_clean()
    link.save(
        update_fields=[
            "is_visible",
            "updated_at",
        ],
    )

    return link


@transaction.atomic
def show_course_material_link(
    *,
    link: CourseMaterialLink,
) -> CourseMaterialLink:
    """
    Показывает материал курса.
    """

    link.is_visible = True
    link.full_clean()
    link.save(
        update_fields=[
            "is_visible",
            "updated_at",
        ],
    )

    return link


def validate_course_material_link_can_be_saved(
    *,
    link: CourseMaterialLink,
) -> None:
    """
    Проверяет, что связь курса с материалом можно сохранить.
    """

    errors: dict[str, str] = {}

    if link.section_id and link.section.course_id != link.course_id:
        errors["section"] = _("Раздел должен относиться к тому же курсу.")

    if link.lesson_id and link.lesson.course_id != link.course_id:
        errors["lesson"] = _("Урок должен относиться к тому же курсу.")

    if link.lesson_id and link.section_id:
        if link.lesson.section_id and link.lesson.section_id != link.section_id:
            errors["lesson"] = _("Урок должен относиться к выбранному разделу.")

    if link.placement == CourseMaterialLink.PlacementChoices.SECTION:
        if not link.section_id:
            errors["section"] = _("Для размещения в разделе нужно указать раздел.")

    if link.placement == CourseMaterialLink.PlacementChoices.LESSON:
        if not link.lesson_id:
            errors["lesson"] = _("Для размещения в уроке нужно указать урок.")

    if errors:
        raise ValidationError(errors)


def _apply_course_material_link_data(
    *,
    link: CourseMaterialLink,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к связи курса с материалом.
    """

    for field_name in COURSE_MATERIAL_LINK_MUTABLE_FIELDS:
        if field_name in data:
            setattr(link, field_name, data[field_name])
