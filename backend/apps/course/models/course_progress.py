from __future__ import annotations

from apps.course.constants import DEFAULT_PROGRESS_PERCENT, DEFAULT_SPENT_MINUTES
from apps.course.managers import CourseProgressManager
from apps.course.validators import validate_progress_dates, validate_progress_percent
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class CourseProgress(models.Model):
    """
    Агрегированный прогресс обучающегося по курсу.
    """

    enrollment = models.OneToOneField(
        "course.CourseEnrollment",
        on_delete=models.CASCADE,
        related_name="progress",
        verbose_name=_("Запись на курс"),
    )

    total_lessons_count = models.PositiveIntegerField(
        _("Всего уроков"),
        default=0,
    )
    completed_lessons_count = models.PositiveIntegerField(
        _("Завершено уроков"),
        default=0,
    )
    required_lessons_count = models.PositiveIntegerField(
        _("Обязательных уроков"),
        default=0,
    )
    completed_required_lessons_count = models.PositiveIntegerField(
        _("Завершено обязательных уроков"),
        default=0,
    )

    progress_percent = models.PositiveSmallIntegerField(
        _("Прогресс, %"),
        default=DEFAULT_PROGRESS_PERCENT,
        validators=[validate_progress_percent],
    )
    spent_minutes = models.PositiveIntegerField(
        _("Затрачено минут"),
        default=DEFAULT_SPENT_MINUTES,
    )

    started_at = models.DateTimeField(
        _("Дата начала"),
        blank=True,
        null=True,
    )
    completed_at = models.DateTimeField(
        _("Дата завершения"),
        blank=True,
        null=True,
    )
    last_activity_at = models.DateTimeField(
        _("Последняя активность"),
        blank=True,
        null=True,
    )
    last_lesson = models.ForeignKey(
        "course.CourseLesson",
        on_delete=models.SET_NULL,
        related_name="last_course_progresses",
        verbose_name=_("Последний урок"),
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        _("Дата создания"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Дата обновления"),
        auto_now=True,
    )

    objects = CourseProgressManager()

    class Meta:
        db_table = "course_progress"
        verbose_name = _("Прогресс курса")
        verbose_name_plural = _("Прогресс курсов")
        ordering = ("-last_activity_at", "-updated_at", "-id")
        indexes = [
            models.Index(
                fields=("progress_percent",), name="course_progress_percent_idx"
            ),
            models.Index(
                fields=("last_activity_at",), name="course_progress_activity_idx"
            ),
        ]

    def __str__(self) -> str:
        return f"Прогресс: {self.enrollment}"

    def clean(self) -> None:
        """
        Проверяет прогресс курса.
        """

        super().clean()

        errors: dict[str, str] = {}

        try:
            validate_progress_dates(
                started_at=self.started_at,
                completed_at=self.completed_at,
            )
        except ValidationError as error:
            errors.update(error.message_dict)

        if self.completed_lessons_count > self.total_lessons_count:
            errors["completed_lessons_count"] = _(
                "Количество завершённых уроков не может превышать общее количество уроков."
            )

        if self.completed_required_lessons_count > self.required_lessons_count:
            errors["completed_required_lessons_count"] = _(
                "Количество завершённых обязательных уроков не может превышать их общее количество."
            )

        if self.last_lesson_id:
            if self.last_lesson.course_id != self.enrollment.course_id:
                errors["last_lesson"] = _(
                    "Последний урок должен относиться к курсу записи."
                )

        if self.progress_percent == 100 and not self.completed_at:
            errors["completed_at"] = _("Для 100% прогресса требуется дата завершения.")

        if errors:
            raise ValidationError(errors)
