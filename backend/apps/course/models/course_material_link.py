from __future__ import annotations

from apps.course.constants import (
    COURSE_MATERIAL_PLACEMENT_COURSE,
    COURSE_MATERIAL_PLACEMENT_LESSON,
    COURSE_MATERIAL_PLACEMENT_MAX_LENGTH,
    COURSE_MATERIAL_PLACEMENT_SECTION,
    DEFAULT_ORDER,
)
from apps.course.managers import CourseMaterialLinkManager
from apps.course.validators import (
    validate_material_link_placement,
    validate_order_value,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class CourseMaterialLink(models.Model):
    """
    Связь курса с материалом из отдельного модуля materials.
    """

    class PlacementChoices(models.TextChoices):
        COURSE = COURSE_MATERIAL_PLACEMENT_COURSE, _("Курс")
        SECTION = COURSE_MATERIAL_PLACEMENT_SECTION, _("Раздел")
        LESSON = COURSE_MATERIAL_PLACEMENT_LESSON, _("Урок")

    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="material_links",
        verbose_name=_("Курс"),
    )
    section = models.ForeignKey(
        "course.CourseSection",
        on_delete=models.CASCADE,
        related_name="material_links",
        verbose_name=_("Раздел"),
        blank=True,
        null=True,
    )
    lesson = models.ForeignKey(
        "course.CourseLesson",
        on_delete=models.CASCADE,
        related_name="material_links",
        verbose_name=_("Урок"),
        blank=True,
        null=True,
    )
    material = models.ForeignKey(
        "materials.Material",
        on_delete=models.CASCADE,
        related_name="course_links",
        verbose_name=_("Материал"),
    )

    placement = models.CharField(
        _("Размещение"),
        max_length=COURSE_MATERIAL_PLACEMENT_MAX_LENGTH,
        choices=PlacementChoices.choices,
        default=PlacementChoices.COURSE,
    )
    order = models.PositiveIntegerField(
        _("Порядок"),
        default=DEFAULT_ORDER,
        validators=[validate_order_value],
    )
    is_required = models.BooleanField(
        _("Обязательный материал"),
        default=False,
    )
    is_visible = models.BooleanField(
        _("Виден"),
        default=True,
    )
    notes = models.TextField(
        _("Примечания"),
        blank=True,
    )

    created_at = models.DateTimeField(
        _("Дата создания"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Дата обновления"),
        auto_now=True,
    )

    objects = CourseMaterialLinkManager()

    class Meta:
        db_table = "course_material_link"
        verbose_name = _("Материал курса")
        verbose_name_plural = _("Материалы курса")
        ordering = ("course", "section__order", "lesson__order", "order", "id")
        constraints = [
            models.UniqueConstraint(
                fields=("course", "section", "lesson", "material"),
                name="course_unique_material_link",
            ),
        ]
        indexes = [
            models.Index(fields=("course",), name="course_material_course_idx"),
            models.Index(fields=("section",), name="course_material_section_idx"),
            models.Index(fields=("lesson",), name="course_material_lesson_idx"),
            models.Index(fields=("material",), name="course_material_material_idx"),
            models.Index(fields=("placement",), name="course_material_place_idx"),
            models.Index(fields=("is_visible",), name="course_material_visible_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.course} — {self.material}"

    def clean(self) -> None:
        """
        Проверяет размещение материала.
        """

        super().clean()

        errors: dict[str, str] = {}

        if self.section_id and self.section.course_id != self.course_id:
            errors["section"] = _("Раздел должен относиться к тому же курсу.")

        if self.lesson_id and self.lesson.course_id != self.course_id:
            errors["lesson"] = _("Урок должен относиться к тому же курсу.")

        if self.lesson_id and self.section_id:
            if self.lesson.section_id and self.lesson.section_id != self.section_id:
                errors["lesson"] = _("Урок должен относиться к выбранному разделу.")

        try:
            validate_material_link_placement(
                placement=self.placement,
                section=self.section,
                lesson=self.lesson,
            )
        except ValidationError as error:
            errors.update(error.message_dict)

        if errors:
            raise ValidationError(errors)
