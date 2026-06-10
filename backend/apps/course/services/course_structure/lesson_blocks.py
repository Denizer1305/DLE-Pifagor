from __future__ import annotations

from typing import Any

from apps.course.models import CourseLessonBlock
from apps.course.selectors import get_course_lesson_block_by_id
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _

COURSE_LESSON_BLOCK_MUTABLE_FIELDS = {
    "lesson",
    "lesson_id",
    "block_type",
    "title",
    "content",
    "external_url",
    "material",
    "material_id",
    "order",
    "is_visible",
}


@transaction.atomic
def create_course_lesson_block(
    *,
    data: dict[str, Any],
) -> CourseLessonBlock:
    """
    Создаёт блок урока.
    """

    block = CourseLessonBlock()

    _apply_course_lesson_block_data(
        block=block,
        data=data,
    )

    validate_course_lesson_block_can_be_saved(block=block)

    block.full_clean()
    block.save()

    return block


@transaction.atomic
def update_course_lesson_block(
    *,
    block: CourseLessonBlock,
    data: dict[str, Any],
) -> CourseLessonBlock:
    """
    Обновляет блок урока.
    """

    _apply_course_lesson_block_data(
        block=block,
        data=data,
    )

    validate_course_lesson_block_can_be_saved(block=block)

    block.full_clean()
    block.save()

    return block


@transaction.atomic
def update_course_lesson_block_by_id(
    *,
    block_id: int,
    data: dict[str, Any],
) -> CourseLessonBlock:
    """
    Обновляет блок урока по идентификатору.
    """

    block = get_course_lesson_block_by_id(block_id)

    return update_course_lesson_block(
        block=block,
        data=data,
    )


@transaction.atomic
def hide_course_lesson_block(
    *,
    block: CourseLessonBlock,
) -> CourseLessonBlock:
    """
    Скрывает блок урока.
    """

    block.is_visible = False
    block.full_clean()
    block.save(
        update_fields=[
            "is_visible",
            "updated_at",
        ],
    )

    return block


@transaction.atomic
def show_course_lesson_block(
    *,
    block: CourseLessonBlock,
) -> CourseLessonBlock:
    """
    Показывает блок урока.
    """

    block.is_visible = True
    block.full_clean()
    block.save(
        update_fields=[
            "is_visible",
            "updated_at",
        ],
    )

    return block


def validate_course_lesson_block_can_be_saved(
    *,
    block: CourseLessonBlock,
) -> None:
    """
    Проверяет, что блок урока можно сохранить.
    """

    errors: dict[str, str] = {}

    if block.block_type == CourseLessonBlock.BlockTypeChoices.MATERIAL:
        if not block.material_id:
            errors["material"] = _("Для блока материала нужно выбрать материал.")

    if block.block_type in {
        CourseLessonBlock.BlockTypeChoices.VIDEO,
        CourseLessonBlock.BlockTypeChoices.LINK,
        CourseLessonBlock.BlockTypeChoices.EMBED,
    }:
        if not block.external_url:
            errors["external_url"] = _("Для этого типа блока нужна внешняя ссылка.")

    if block.block_type in {
        CourseLessonBlock.BlockTypeChoices.TEXT,
        CourseLessonBlock.BlockTypeChoices.CODE,
    }:
        if not block.content:
            errors["content"] = _(
                "Для текстового блока или блока кода нужно содержимое."
            )

    if errors:
        raise ValidationError(errors)


def _apply_course_lesson_block_data(
    *,
    block: CourseLessonBlock,
    data: dict[str, Any],
) -> None:
    """
    Применяет входные данные к блоку урока.
    """

    for field_name in COURSE_LESSON_BLOCK_MUTABLE_FIELDS:
        if field_name in data:
            setattr(block, field_name, data[field_name])
