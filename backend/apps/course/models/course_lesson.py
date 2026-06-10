from __future__ import annotations

from apps.course.constants import (
    COURSE_LESSON_TITLE_MAX_LENGTH,
    COURSE_LESSON_TYPE_MAX_LENGTH,
    DEFAULT_HOURS,
    DEFAULT_ORDER,
    LESSON_TYPE_CONSULTATION,
    LESSON_TYPE_CONTROL,
    LESSON_TYPE_INDEPENDENT,
    LESSON_TYPE_LAB,
    LESSON_TYPE_LECTURE,
    LESSON_TYPE_LESSON,
    LESSON_TYPE_OTHER,
    LESSON_TYPE_PRACTICE,
    LESSON_TYPE_SEMINAR,
)
from apps.course.managers import CourseLessonManager
from apps.course.validators import validate_lesson_hours, validate_order_value
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class CourseLesson(models.Model):
    """
    Урок курса.

    В академическом курсе соответствует строке КТП:
    номер занятия, вид занятия, тема, часы, литература,
    самостоятельная работа и примечания.
    """

    class LessonTypeChoices(models.TextChoices):
        LESSON = LESSON_TYPE_LESSON, _("Урок")
        LECTURE = LESSON_TYPE_LECTURE, _("Лекция")
        PRACTICE = LESSON_TYPE_PRACTICE, _("Практическое занятие")
        LAB = LESSON_TYPE_LAB, _("Лабораторная работа")
        SEMINAR = LESSON_TYPE_SEMINAR, _("Семинар")
        CONTROL = LESSON_TYPE_CONTROL, _("Контрольная работа")
        CONSULTATION = LESSON_TYPE_CONSULTATION, _("Консультация")
        INDEPENDENT = LESSON_TYPE_INDEPENDENT, _("Самостоятельная работа")
        OTHER = LESSON_TYPE_OTHER, _("Иное занятие")

    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="lessons",
        verbose_name=_("Курс"),
    )
    section = models.ForeignKey(
        "course.CourseSection",
        on_delete=models.SET_NULL,
        related_name="lessons",
        verbose_name=_("Раздел"),
        blank=True,
        null=True,
    )

    lesson_number = models.PositiveIntegerField(
        _("Номер занятия"),
        blank=True,
        null=True,
    )
    lesson_type = models.CharField(
        _("Вид занятия"),
        max_length=COURSE_LESSON_TYPE_MAX_LENGTH,
        choices=LessonTypeChoices.choices,
        default=LessonTypeChoices.LESSON,
    )
    title = models.CharField(
        _("Тема занятия"),
        max_length=COURSE_LESSON_TITLE_MAX_LENGTH,
    )
    short_content = models.TextField(
        _("Краткое содержание"),
        blank=True,
    )

    planned_hours = models.PositiveIntegerField(
        _("Плановые часы"),
        default=DEFAULT_HOURS,
    )
    theory_hours = models.PositiveIntegerField(
        _("Теоретические часы"),
        default=DEFAULT_HOURS,
    )
    practice_hours = models.PositiveIntegerField(
        _("Практические часы"),
        default=DEFAULT_HOURS,
    )
    lab_hours = models.PositiveIntegerField(
        _("Лабораторные часы"),
        default=DEFAULT_HOURS,
    )
    self_study_hours = models.PositiveIntegerField(
        _("Самостоятельная работа"),
        default=DEFAULT_HOURS,
    )

    visual_aids = models.TextField(
        _("Наглядные пособия и приборы"),
        blank=True,
    )
    literature = models.TextField(
        _("Учебники и литература"),
        blank=True,
    )
    independent_work = models.TextField(
        _("Задания для самостоятельной работы"),
        blank=True,
    )
    notes = models.TextField(
        _("Примечания"),
        blank=True,
    )

    order = models.PositiveIntegerField(
        _("Порядок"),
        default=DEFAULT_ORDER,
        validators=[validate_order_value],
    )
    available_from = models.DateTimeField(
        _("Доступен с"),
        blank=True,
        null=True,
    )

    is_required = models.BooleanField(
        _("Обязательный урок"),
        default=True,
    )
    is_preview = models.BooleanField(
        _("Доступен для предпросмотра"),
        default=False,
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

    objects = CourseLessonManager()

    class Meta:
        db_table = "course_lesson"
        verbose_name = _("Урок курса")
        verbose_name_plural = _("Уроки курса")
        ordering = ("course", "section__order", "order", "lesson_number")
        constraints = [
            models.UniqueConstraint(
                fields=("course", "lesson_number"),
                condition=models.Q(lesson_number__isnull=False),
                name="course_unique_lesson_number",
            ),
            models.UniqueConstraint(
                fields=("section", "order"),
                condition=models.Q(section__isnull=False),
                name="course_unique_lesson_order_in_section",
            ),
        ]
        indexes = [
            models.Index(fields=("course",), name="course_lesson_course_idx"),
            models.Index(fields=("section",), name="course_lesson_section_idx"),
            models.Index(fields=("lesson_type",), name="course_lesson_type_idx"),
            models.Index(fields=("is_published",), name="course_lesson_pub_idx"),
            models.Index(fields=("is_active",), name="course_lesson_active_idx"),
            models.Index(fields=("order",), name="course_lesson_order_idx"),
        ]

    def __str__(self) -> str:
        if self.lesson_number:
            return f"{self.lesson_number}. {self.title}"

        return self.title

    def clean(self) -> None:
        """
        Проверяет согласованность урока.
        """

        super().clean()

        errors: dict[str, str] = {}

        if self.section_id and self.course_id:
            if self.section.course_id != self.course_id:
                errors["section"] = _("Раздел должен относиться к тому же курсу.")

        try:
            validate_lesson_hours(
                planned_hours=self.planned_hours,
                theory_hours=self.theory_hours,
                practice_hours=self.practice_hours,
                lab_hours=self.lab_hours,
                self_study_hours=self.self_study_hours,
            )
        except ValidationError as error:
            errors.update(error.message_dict)

        if errors:
            raise ValidationError(errors)
