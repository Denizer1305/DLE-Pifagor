from __future__ import annotations

from apps.course.constants import (
    COURSE_GROUP_VISIBILITY_ARCHIVED,
    COURSE_GROUP_VISIBILITY_HIDDEN,
    COURSE_GROUP_VISIBILITY_MAX_LENGTH,
    COURSE_GROUP_VISIBILITY_VISIBLE,
)
from apps.course.managers import CourseGroupAccessManager
from apps.course.validators import (
    validate_access_date_range,
    validate_course_group_access_relations,
)
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class CourseGroupAccess(models.Model):
    """
    Доступ учебной группы к курсу.

    Через эту модель один курс преподавателя может быть открыт
    нескольким учебным группам.
    """

    class VisibilityChoices(models.TextChoices):
        HIDDEN = COURSE_GROUP_VISIBILITY_HIDDEN, _("Скрыт")
        VISIBLE = COURSE_GROUP_VISIBILITY_VISIBLE, _("Виден")
        ARCHIVED = COURSE_GROUP_VISIBILITY_ARCHIVED, _("Архивирован")

    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="group_accesses",
        verbose_name=_("Курс"),
    )
    group = models.ForeignKey(
        "organizations.StudyGroup",
        on_delete=models.CASCADE,
        related_name="course_accesses",
        verbose_name=_("Учебная группа"),
    )
    group_subject = models.ForeignKey(
        "education.GroupSubject",
        on_delete=models.PROTECT,
        related_name="course_group_accesses",
        verbose_name=_("Предмет группы"),
        blank=True,
        null=True,
    )
    teacher_group_subject = models.ForeignKey(
        "education.TeacherGroupSubject",
        on_delete=models.PROTECT,
        related_name="course_group_accesses",
        verbose_name=_("Назначение преподавателя"),
        blank=True,
        null=True,
    )

    visibility = models.CharField(
        _("Видимость для группы"),
        max_length=COURSE_GROUP_VISIBILITY_MAX_LENGTH,
        choices=VisibilityChoices.choices,
        default=VisibilityChoices.HIDDEN,
    )
    starts_at = models.DateField(
        _("Дата начала доступа"),
        blank=True,
        null=True,
    )
    ends_at = models.DateField(
        _("Дата окончания доступа"),
        blank=True,
        null=True,
    )
    auto_enroll = models.BooleanField(
        _("Автоматически записывать учащихся"),
        default=True,
    )
    is_active = models.BooleanField(
        _("Активен"),
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

    objects = CourseGroupAccessManager()

    class Meta:
        db_table = "course_group_access"
        verbose_name = _("Доступ группы к курсу")
        verbose_name_plural = _("Доступы групп к курсам")
        ordering = ("course", "group__name", "group__code")
        constraints = [
            models.UniqueConstraint(
                fields=("course", "group"),
                name="course_unique_group_access",
            ),
            models.UniqueConstraint(
                fields=("course", "group_subject"),
                condition=models.Q(group_subject__isnull=False),
                name="course_unique_group_subject_access",
            ),
        ]
        indexes = [
            models.Index(fields=("course",), name="course_group_access_course_idx"),
            models.Index(fields=("group",), name="course_group_access_group_idx"),
            models.Index(fields=("visibility",), name="course_group_access_vis_idx"),
            models.Index(fields=("is_active",), name="course_group_access_active_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.course} — {self.group}"

    def clean(self) -> None:
        """
        Проверяет доступ группы к курсу.
        """

        super().clean()

        errors: dict[str, str] = {}

        try:
            validate_access_date_range(
                starts_at=self.starts_at,
                ends_at=self.ends_at,
            )
        except ValidationError as error:
            errors.update(error.message_dict)

        if self.course_id:
            try:
                validate_course_group_access_relations(
                    course=self.course,
                    group=self.group,
                    group_subject=self.group_subject,
                    teacher_group_subject=self.teacher_group_subject,
                )
            except ValidationError as error:
                errors.update(error.message_dict)

        if self.visibility == self.VisibilityChoices.ARCHIVED:
            self.is_active = False

        if errors:
            raise ValidationError(errors)
