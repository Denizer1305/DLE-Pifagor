from __future__ import annotations

from apps.course.constants import (
    COURSE_ACCESS_CODE_MAX_LENGTH,
    COURSE_ACCESS_TYPE_INVITE_CODE,
    COURSE_ACCESS_TYPE_LEARNER,
    COURSE_ACCESS_TYPE_MAX_LENGTH,
    COURSE_ACCESS_TYPE_ORGANIZATION,
    COURSE_ACCESS_TYPE_PUBLIC_LINK,
)
from apps.course.managers import CourseAccessRuleManager
from apps.course.validators import (
    validate_access_date_range,
    validate_course_access_rule_payload,
)
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class CourseAccessRule(models.Model):
    """
    Нестандартное правило доступа к курсу.

    Используется для авторских, факультативных, экзаменационных курсов,
    индивидуального доступа, доступа по коду и публичной ссылке.
    """

    class AccessTypeChoices(models.TextChoices):
        LEARNER = COURSE_ACCESS_TYPE_LEARNER, _("Персональный доступ")
        ORGANIZATION = COURSE_ACCESS_TYPE_ORGANIZATION, _("Доступ организации")
        PUBLIC_LINK = COURSE_ACCESS_TYPE_PUBLIC_LINK, _("Публичная ссылка")
        INVITE_CODE = COURSE_ACCESS_TYPE_INVITE_CODE, _("Код приглашения")

    course = models.ForeignKey(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="access_rules",
        verbose_name=_("Курс"),
    )
    access_type = models.CharField(
        _("Тип доступа"),
        max_length=COURSE_ACCESS_TYPE_MAX_LENGTH,
        choices=AccessTypeChoices.choices,
    )

    learner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_access_rules",
        verbose_name=_("Обучающийся"),
        blank=True,
        null=True,
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="course_access_rules",
        verbose_name=_("Организация"),
        blank=True,
        null=True,
    )
    access_code = models.CharField(
        _("Код доступа"),
        max_length=COURSE_ACCESS_CODE_MAX_LENGTH,
        blank=True,
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
        _("Автоматически записывать"),
        default=False,
    )
    is_active = models.BooleanField(
        _("Активно"),
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

    objects = CourseAccessRuleManager()

    class Meta:
        db_table = "course_access_rule"
        verbose_name = _("Правило доступа к курсу")
        verbose_name_plural = _("Правила доступа к курсам")
        ordering = ("course", "access_type", "id")
        constraints = [
            models.UniqueConstraint(
                fields=("course", "learner"),
                condition=models.Q(
                    access_type=COURSE_ACCESS_TYPE_LEARNER,
                    learner__isnull=False,
                ),
                name="course_unique_learner_access_rule",
            ),
            models.UniqueConstraint(
                fields=("course", "organization"),
                condition=models.Q(
                    access_type=COURSE_ACCESS_TYPE_ORGANIZATION,
                    organization__isnull=False,
                ),
                name="course_unique_org_access_rule",
            ),
            models.UniqueConstraint(
                fields=("access_code",),
                condition=(
                    models.Q(access_type=COURSE_ACCESS_TYPE_PUBLIC_LINK)
                    | models.Q(access_type=COURSE_ACCESS_TYPE_INVITE_CODE)
                )
                & ~models.Q(access_code=""),
                name="course_unique_access_code_rule",
            ),
        ]
        indexes = [
            models.Index(fields=("course",), name="course_access_rule_course_idx"),
            models.Index(fields=("access_type",), name="course_access_rule_type_idx"),
            models.Index(fields=("learner",), name="course_access_rule_learner_idx"),
            models.Index(fields=("organization",), name="course_access_rule_org_idx"),
            models.Index(fields=("is_active",), name="course_access_rule_active_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.course} — {self.get_access_type_display()}"

    def clean(self) -> None:
        """
        Проверяет правило доступа.
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

        try:
            validate_course_access_rule_payload(
                access_type=self.access_type,
                learner=self.learner,
                organization=self.organization,
                access_code=self.access_code,
            )
        except ValidationError as error:
            errors.update(error.message_dict)

        if errors:
            raise ValidationError(errors)
