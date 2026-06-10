from __future__ import annotations

from apps.course.constants import (
    COURSE_SECTION_TITLE_MAX_LENGTH,
    DEFAULT_HOURS,
    DEFAULT_ORDER,
)
from apps.course.managers import CourseSectionManager
from apps.course.validators import validate_hours_value, validate_order_value
from django.db import models
from django.utils.translation import gettext_lazy as _


class CourseSection(models.Model):
    """
    Раздел курса / раздел КТП.
    """

    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="sections",
        verbose_name=_("Курс"),
    )
    title = models.CharField(
        _("Название раздела"),
        max_length=COURSE_SECTION_TITLE_MAX_LENGTH,
    )
    description = models.TextField(
        _("Описание"),
        blank=True,
    )
    section_number = models.PositiveIntegerField(
        _("Номер раздела"),
        blank=True,
        null=True,
    )
    order = models.PositiveIntegerField(
        _("Порядок"),
        default=DEFAULT_ORDER,
        validators=[validate_order_value],
    )
    planned_hours = models.PositiveIntegerField(
        _("Плановые часы"),
        default=DEFAULT_HOURS,
        validators=[validate_hours_value],
    )
    is_required = models.BooleanField(
        _("Обязательный раздел"),
        default=True,
    )
    is_published = models.BooleanField(
        _("Опубликован"),
        default=False,
    )
    is_active = models.BooleanField(
        _("Активен"),
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

    objects = CourseSectionManager()

    class Meta:
        db_table = "course_section"
        verbose_name = _("Раздел курса")
        verbose_name_plural = _("Разделы курса")
        ordering = ("course", "order", "section_number", "title")
        constraints = [
            models.UniqueConstraint(
                fields=("course", "order"),
                name="course_unique_section_order",
            ),
            models.UniqueConstraint(
                fields=("course", "section_number"),
                condition=models.Q(section_number__isnull=False),
                name="course_unique_section_number",
            ),
        ]
        indexes = [
            models.Index(fields=("course",), name="course_section_course_idx"),
            models.Index(fields=("order",), name="course_section_order_idx"),
            models.Index(fields=("is_published",), name="course_section_pub_idx"),
            models.Index(fields=("is_active",), name="course_section_active_idx"),
        ]

    def __str__(self) -> str:
        return self.title
