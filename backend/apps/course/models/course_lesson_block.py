from __future__ import annotations

from apps.course.constants import (
    COURSE_LESSON_BLOCK_TITLE_MAX_LENGTH,
    COURSE_LESSON_BLOCK_TYPE_MAX_LENGTH,
    DEFAULT_ORDER,
    LESSON_BLOCK_TYPE_ASSIGNMENT_PLACEHOLDER,
    LESSON_BLOCK_TYPE_CODE,
    LESSON_BLOCK_TYPE_EMBED,
    LESSON_BLOCK_TYPE_FILE,
    LESSON_BLOCK_TYPE_IMAGE,
    LESSON_BLOCK_TYPE_LINK,
    LESSON_BLOCK_TYPE_MATERIAL,
    LESSON_BLOCK_TYPE_PRESENTATION,
    LESSON_BLOCK_TYPE_TEXT,
    LESSON_BLOCK_TYPE_VIDEO,
)
from apps.course.managers import CourseLessonBlockManager
from apps.course.validators import validate_order_value
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class CourseLessonBlock(models.Model):
    """
    Блок урока.

    Урок собирается из блоков: текст, видео, ссылка, материал,
    код, презентация или задел под будущий assignment.
    """

    class BlockTypeChoices(models.TextChoices):
        TEXT = LESSON_BLOCK_TYPE_TEXT, _("Текст")
        VIDEO = LESSON_BLOCK_TYPE_VIDEO, _("Видео")
        FILE = LESSON_BLOCK_TYPE_FILE, _("Файл")
        LINK = LESSON_BLOCK_TYPE_LINK, _("Ссылка")
        IMAGE = LESSON_BLOCK_TYPE_IMAGE, _("Изображение")
        PRESENTATION = LESSON_BLOCK_TYPE_PRESENTATION, _("Презентация")
        CODE = LESSON_BLOCK_TYPE_CODE, _("Код")
        EMBED = LESSON_BLOCK_TYPE_EMBED, _("Встраиваемый блок")
        MATERIAL = LESSON_BLOCK_TYPE_MATERIAL, _("Материал")
        ASSIGNMENT_PLACEHOLDER = (
            LESSON_BLOCK_TYPE_ASSIGNMENT_PLACEHOLDER,
            _("Место для задания"),
        )

    lesson = models.ForeignKey(
        "course.CourseLesson",
        on_delete=models.CASCADE,
        related_name="blocks",
        verbose_name=_("Урок"),
    )
    block_type = models.CharField(
        _("Тип блока"),
        max_length=COURSE_LESSON_BLOCK_TYPE_MAX_LENGTH,
        choices=BlockTypeChoices.choices,
        default=BlockTypeChoices.TEXT,
    )
    title = models.CharField(
        _("Заголовок блока"),
        max_length=COURSE_LESSON_BLOCK_TITLE_MAX_LENGTH,
        blank=True,
    )
    content = models.TextField(
        _("Содержимое"),
        blank=True,
    )
    external_url = models.URLField(
        _("Внешняя ссылка"),
        blank=True,
    )
    material = models.ForeignKey(
        "materials.Material",
        on_delete=models.SET_NULL,
        related_name="course_lesson_blocks",
        verbose_name=_("Материал"),
        blank=True,
        null=True,
    )

    order = models.PositiveIntegerField(
        _("Порядок"),
        default=DEFAULT_ORDER,
        validators=[validate_order_value],
    )
    is_visible = models.BooleanField(
        _("Виден"),
        default=True,
    )

    created_at = models.DateTimeField(
        _("Дата создания"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Дата обновления"),
        auto_now=True,
    )

    objects = CourseLessonBlockManager()

    class Meta:
        db_table = "course_lesson_block"
        verbose_name = _("Блок урока")
        verbose_name_plural = _("Блоки уроков")
        ordering = ("lesson", "order", "id")
        constraints = [
            models.UniqueConstraint(
                fields=("lesson", "order"),
                name="course_unique_lesson_block_order",
            ),
        ]
        indexes = [
            models.Index(fields=("lesson",), name="course_block_lesson_idx"),
            models.Index(fields=("block_type",), name="course_block_type_idx"),
            models.Index(fields=("is_visible",), name="course_block_visible_idx"),
        ]

    def __str__(self) -> str:
        return self.title or f"{self.lesson} — {self.get_block_type_display()}"

    def clean(self) -> None:
        """
        Проверяет содержимое блока.
        """

        super().clean()

        errors: dict[str, str] = {}

        if self.block_type == self.BlockTypeChoices.MATERIAL and not self.material_id:
            errors["material"] = _("Для блока материала нужно выбрать материал.")

        if (
            self.block_type
            in {
                self.BlockTypeChoices.VIDEO,
                self.BlockTypeChoices.LINK,
                self.BlockTypeChoices.EMBED,
            }
            and not self.external_url
        ):
            errors["external_url"] = _("Для этого типа блока нужна ссылка.")

        if self.block_type == self.BlockTypeChoices.TEXT and not self.content:
            errors["content"] = _("Для текстового блока нужно содержимое.")

        if errors:
            raise ValidationError(errors)
