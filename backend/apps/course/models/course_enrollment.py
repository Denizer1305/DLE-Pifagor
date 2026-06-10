from __future__ import annotations

from apps.course.constants import (
    COURSE_ENROLLMENT_STATUS_ARCHIVED,
    COURSE_ENROLLMENT_STATUS_CANCELLED,
    COURSE_ENROLLMENT_STATUS_COMPLETED,
    COURSE_ENROLLMENT_STATUS_ENROLLED,
    COURSE_ENROLLMENT_STATUS_IN_PROGRESS,
    COURSE_ENROLLMENT_STATUS_MAX_LENGTH,
    DEFAULT_PROGRESS_PERCENT,
)
from apps.course.managers import CourseEnrollmentManager
from apps.course.validators import validate_progress_percent
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CourseEnrollment(models.Model):
    """
    Запись обучающегося на курс.
    """

    class StatusChoices(models.TextChoices):
        ENROLLED = COURSE_ENROLLMENT_STATUS_ENROLLED, _("Зачислен")
        IN_PROGRESS = COURSE_ENROLLMENT_STATUS_IN_PROGRESS, _("В процессе")
        COMPLETED = COURSE_ENROLLMENT_STATUS_COMPLETED, _("Завершён")
        CANCELLED = COURSE_ENROLLMENT_STATUS_CANCELLED, _("Отменён")
        ARCHIVED = COURSE_ENROLLMENT_STATUS_ARCHIVED, _("Архивирован")

    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name=_("Курс"),
    )
    learner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_enrollments",
        verbose_name=_("Обучающийся"),
    )
    group_access = models.ForeignKey(
        "course.CourseGroupAccess",
        on_delete=models.SET_NULL,
        related_name="enrollments",
        verbose_name=_("Групповой доступ"),
        blank=True,
        null=True,
    )
    access_rule = models.ForeignKey(
        "course.CourseAccessRule",
        on_delete=models.SET_NULL,
        related_name="enrollments",
        verbose_name=_("Правило доступа"),
        blank=True,
        null=True,
    )

    status = models.CharField(
        _("Статус"),
        max_length=COURSE_ENROLLMENT_STATUS_MAX_LENGTH,
        choices=StatusChoices.choices,
        default=StatusChoices.ENROLLED,
    )
    enrolled_at = models.DateTimeField(
        _("Дата записи"),
        default=timezone.now,
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
    progress_percent = models.PositiveSmallIntegerField(
        _("Прогресс, %"),
        default=DEFAULT_PROGRESS_PERCENT,
        validators=[validate_progress_percent],
    )

    created_at = models.DateTimeField(
        _("Дата создания"),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _("Дата обновления"),
        auto_now=True,
    )

    objects = CourseEnrollmentManager()

    class Meta:
        db_table = "course_enrollment"
        verbose_name = _("Запись на курс")
        verbose_name_plural = _("Записи на курсы")
        ordering = ("-last_activity_at", "-enrolled_at", "-id")
        constraints = [
            models.UniqueConstraint(
                fields=("course", "learner"),
                name="course_unique_learner_enrollment",
            ),
        ]
        indexes = [
            models.Index(fields=("course",), name="course_enrollment_course_idx"),
            models.Index(fields=("learner",), name="course_enrollment_learner_idx"),
            models.Index(fields=("status",), name="course_enrollment_status_idx"),
            models.Index(fields=("group_access",), name="course_enroll_group_idx"),
            models.Index(fields=("access_rule",), name="course_enroll_rule_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.learner} — {self.course}"

    def clean(self) -> None:
        """
        Проверяет запись обучающегося на курс.
        """

        super().clean()

        errors: dict[str, str] = {}

        if self.group_access_id and self.group_access.course_id != self.course_id:
            errors["group_access"] = _(
                "Групповой доступ должен относиться к тому же курсу."
            )

        if self.access_rule_id and self.access_rule.course_id != self.course_id:
            errors["access_rule"] = _(
                "Правило доступа должно относиться к тому же курсу."
            )

        if self.completed_at and self.started_at:
            if self.completed_at < self.started_at:
                errors["completed_at"] = _(
                    "Дата завершения не может быть раньше даты начала."
                )

        if self.status == self.StatusChoices.IN_PROGRESS and not self.started_at:
            self.started_at = timezone.now()

        if self.status == self.StatusChoices.COMPLETED:
            self.progress_percent = 100

            if not self.completed_at:
                self.completed_at = timezone.now()

        if (
            self.status
            in {
                self.StatusChoices.CANCELLED,
                self.StatusChoices.ARCHIVED,
            }
            and self.progress_percent == 100
        ):
            errors["progress_percent"] = _(
                "Отменённая или архивная запись не должна иметь 100% прогресса."
            )

        if errors:
            raise ValidationError(errors)
