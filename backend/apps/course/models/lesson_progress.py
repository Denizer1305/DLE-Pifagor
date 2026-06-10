from __future__ import annotations

from apps.course.constants import (
    DEFAULT_ATTEMPTS_COUNT,
    DEFAULT_SPENT_MINUTES,
    LESSON_PROGRESS_STATUS_COMPLETED,
    LESSON_PROGRESS_STATUS_IN_PROGRESS,
    LESSON_PROGRESS_STATUS_MAX_LENGTH,
    LESSON_PROGRESS_STATUS_NOT_STARTED,
    LESSON_PROGRESS_STATUS_SKIPPED,
)
from apps.course.managers import LessonProgressManager
from apps.course.validators import (
    validate_lesson_progress_course_consistency,
    validate_progress_dates,
    validate_score_value,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class LessonProgress(models.Model):
    """
    Прогресс обучающегося по конкретному уроку.
    """

    class StatusChoices(models.TextChoices):
        NOT_STARTED = LESSON_PROGRESS_STATUS_NOT_STARTED, _("Не начат")
        IN_PROGRESS = LESSON_PROGRESS_STATUS_IN_PROGRESS, _("В процессе")
        COMPLETED = LESSON_PROGRESS_STATUS_COMPLETED, _("Завершён")
        SKIPPED = LESSON_PROGRESS_STATUS_SKIPPED, _("Пропущен")

    enrollment = models.ForeignKey(
        "course.CourseEnrollment",
        on_delete=models.CASCADE,
        related_name="lesson_progresses",
        verbose_name=_("Запись на курс"),
    )
    course_progress = models.ForeignKey(
        "course.CourseProgress",
        on_delete=models.CASCADE,
        related_name="lesson_progresses",
        verbose_name=_("Прогресс курса"),
    )
    lesson = models.ForeignKey(
        "course.CourseLesson",
        on_delete=models.CASCADE,
        related_name="progresses",
        verbose_name=_("Урок"),
    )

    status = models.CharField(
        _("Статус"),
        max_length=LESSON_PROGRESS_STATUS_MAX_LENGTH,
        choices=StatusChoices.choices,
        default=StatusChoices.NOT_STARTED,
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
    last_viewed_at = models.DateTimeField(
        _("Последний просмотр"),
        blank=True,
        null=True,
    )

    spent_minutes = models.PositiveIntegerField(
        _("Затрачено минут"),
        default=DEFAULT_SPENT_MINUTES,
    )
    attempts_count = models.PositiveIntegerField(
        _("Количество попыток"),
        default=DEFAULT_ATTEMPTS_COUNT,
    )
    score = models.PositiveSmallIntegerField(
        _("Балл"),
        blank=True,
        null=True,
        validators=[validate_score_value],
    )

    created_at = models.DateTimeField(
        _("Дата создания"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Дата обновления"),
        auto_now=True,
    )

    objects = LessonProgressManager()

    class Meta:
        db_table = "course_lesson_progress"
        verbose_name = _("Прогресс урока")
        verbose_name_plural = _("Прогресс уроков")
        ordering = (
            "lesson__section__order",
            "lesson__order",
            "lesson__lesson_number",
        )
        constraints = [
            models.UniqueConstraint(
                fields=("enrollment", "lesson"),
                name="course_unique_lesson_progress",
            ),
        ]
        indexes = [
            models.Index(fields=("enrollment",), name="course_lesson_prog_enroll_idx"),
            models.Index(
                fields=("course_progress",), name="course_lesson_prog_course_idx"
            ),
            models.Index(fields=("lesson",), name="course_lesson_prog_lesson_idx"),
            models.Index(fields=("status",), name="course_lesson_prog_status_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.enrollment} — {self.lesson}"

    def clean(self) -> None:
        """
        Проверяет прогресс урока.
        """

        super().clean()

        errors: dict[str, str] = {}

        try:
            validate_lesson_progress_course_consistency(
                enrollment=self.enrollment,
                lesson=self.lesson,
            )
        except ValidationError as error:
            errors.update(error.message_dict)

        try:
            validate_progress_dates(
                started_at=self.started_at,
                completed_at=self.completed_at,
            )
        except ValidationError as error:
            errors.update(error.message_dict)

        if self.course_progress_id:
            if self.course_progress.enrollment_id != self.enrollment_id:
                errors["course_progress"] = _(
                    "Прогресс курса должен относиться к той же записи на курс."
                )

        if self.status == self.StatusChoices.IN_PROGRESS and not self.started_at:
            self.started_at = timezone.now()

        if self.status == self.StatusChoices.COMPLETED:
            if not self.started_at:
                self.started_at = timezone.now()

            if not self.completed_at:
                self.completed_at = timezone.now()

            self.last_viewed_at = self.completed_at

        if errors:
            raise ValidationError(errors)
