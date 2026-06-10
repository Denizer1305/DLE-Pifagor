from __future__ import annotations

import uuid

from apps.course.constants import (
    COURSE_CODE_MAX_LENGTH,
    COURSE_LANGUAGE_MAX_LENGTH,
    COURSE_LEVEL_MAX_LENGTH,
    COURSE_ORIGIN_EDUCATION_LOAD,
    COURSE_ORIGIN_KTP_IMPORT,
    COURSE_ORIGIN_MANUAL,
    COURSE_ORIGIN_MAX_LENGTH,
    COURSE_ORIGIN_TEMPLATE,
    COURSE_SLUG_MAX_LENGTH,
    COURSE_STATUS_ARCHIVED,
    COURSE_STATUS_DRAFT,
    COURSE_STATUS_MAX_LENGTH,
    COURSE_STATUS_PUBLISHED,
    COURSE_SUBTITLE_MAX_LENGTH,
    COURSE_TITLE_MAX_LENGTH,
    COURSE_TYPE_ACADEMIC,
    COURSE_TYPE_AUTHOR,
    COURSE_TYPE_CLUB,
    COURSE_TYPE_ELECTIVE,
    COURSE_TYPE_EXAM_PREP,
    COURSE_TYPE_INTENSIVE,
    COURSE_TYPE_MAX_LENGTH,
    COURSE_VISIBILITY_ASSIGNED_ONLY,
    COURSE_VISIBILITY_MAX_LENGTH,
    COURSE_VISIBILITY_ORGANIZATION,
    COURSE_VISIBILITY_PRIVATE,
    COURSE_VISIBILITY_PUBLIC_LINK,
    DEFAULT_COURSE_LANGUAGE,
)
from apps.course.managers import CourseManager
from apps.course.validators import (
    validate_course_code,
    validate_course_date_range,
    validate_course_publication_dates,
    validate_course_slug,
)
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Course(models.Model):
    """
    Курс платформы.

    Курс является рабочей прослойкой между академической нагрузкой
    из education, учебными материалами из materials и будущими заданиями
    из assignments.

    Академический курс создаётся под преподавателя и может быть открыт
    нескольким учебным группам через CourseGroupAccess.
    """

    class CourseTypeChoices(models.TextChoices):
        ACADEMIC = COURSE_TYPE_ACADEMIC, _("Академический")
        AUTHOR = COURSE_TYPE_AUTHOR, _("Авторский")
        EXAM_PREP = COURSE_TYPE_EXAM_PREP, _("Подготовка к экзамену")
        INTENSIVE = COURSE_TYPE_INTENSIVE, _("Интенсив")
        CLUB = COURSE_TYPE_CLUB, _("Кружок / клуб")
        ELECTIVE = COURSE_TYPE_ELECTIVE, _("Факультатив")

    class OriginChoices(models.TextChoices):
        MANUAL = COURSE_ORIGIN_MANUAL, _("Создан вручную")
        KTP_IMPORT = COURSE_ORIGIN_KTP_IMPORT, _("Импортирован из КТП")
        EDUCATION_LOAD = COURSE_ORIGIN_EDUCATION_LOAD, _("Создан из нагрузки")
        TEMPLATE = COURSE_ORIGIN_TEMPLATE, _("Создан из шаблона")

    class StatusChoices(models.TextChoices):
        DRAFT = COURSE_STATUS_DRAFT, _("Черновик")
        PUBLISHED = COURSE_STATUS_PUBLISHED, _("Опубликован")
        ARCHIVED = COURSE_STATUS_ARCHIVED, _("Архивирован")

    class VisibilityChoices(models.TextChoices):
        PRIVATE = COURSE_VISIBILITY_PRIVATE, _("Приватный")
        ASSIGNED_ONLY = COURSE_VISIBILITY_ASSIGNED_ONLY, _("Только назначенным")
        ORGANIZATION = COURSE_VISIBILITY_ORGANIZATION, _("Внутри организации")
        PUBLIC_LINK = COURSE_VISIBILITY_PUBLIC_LINK, _("По публичной ссылке")

    uid = models.UUIDField(
        _("Публичный идентификатор"),
        default=uuid.uuid4,
        unique=True,
        editable=False,
    )
    code = models.CharField(
        _("Код курса"),
        max_length=COURSE_CODE_MAX_LENGTH,
        unique=True,
        validators=[validate_course_code],
    )
    slug = models.SlugField(
        _("Slug"),
        max_length=COURSE_SLUG_MAX_LENGTH,
        unique=True,
        validators=[validate_course_slug],
    )

    title = models.CharField(
        _("Название"),
        max_length=COURSE_TITLE_MAX_LENGTH,
    )
    subtitle = models.CharField(
        _("Краткий подзаголовок"),
        max_length=COURSE_SUBTITLE_MAX_LENGTH,
        blank=True,
    )
    description = models.TextField(
        _("Описание"),
        blank=True,
    )

    course_type = models.CharField(
        _("Тип курса"),
        max_length=COURSE_TYPE_MAX_LENGTH,
        choices=CourseTypeChoices.choices,
        default=CourseTypeChoices.ACADEMIC,
    )
    origin = models.CharField(
        _("Источник курса"),
        max_length=COURSE_ORIGIN_MAX_LENGTH,
        choices=OriginChoices.choices,
        default=OriginChoices.MANUAL,
    )
    status = models.CharField(
        _("Статус"),
        max_length=COURSE_STATUS_MAX_LENGTH,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
    )
    visibility = models.CharField(
        _("Видимость"),
        max_length=COURSE_VISIBILITY_MAX_LENGTH,
        choices=VisibilityChoices.choices,
        default=VisibilityChoices.PRIVATE,
    )

    level = models.CharField(
        _("Уровень"),
        max_length=COURSE_LEVEL_MAX_LENGTH,
        blank=True,
    )
    language = models.CharField(
        _("Язык курса"),
        max_length=COURSE_LANGUAGE_MAX_LENGTH,
        default=DEFAULT_COURSE_LANGUAGE,
    )

    owner_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="owned_courses",
        verbose_name=_("Владелец-преподаватель"),
    )
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="courses",
        verbose_name=_("Организация"),
        blank=True,
        null=True,
    )
    subject = models.ForeignKey(
        "organizations.Subject",
        on_delete=models.PROTECT,
        related_name="courses",
        verbose_name=_("Предмет"),
        blank=True,
        null=True,
    )
    academic_year = models.ForeignKey(
        "education.AcademicYear",
        on_delete=models.PROTECT,
        related_name="courses",
        verbose_name=_("Учебный год"),
        blank=True,
        null=True,
    )
    period = models.ForeignKey(
        "education.EducationPeriod",
        on_delete=models.PROTECT,
        related_name="courses",
        verbose_name=_("Учебный период"),
        blank=True,
        null=True,
    )

    cover_image = models.FileField(
        _("Обложка курса"),
        upload_to="course/covers/",
        blank=True,
        null=True,
    )

    is_template = models.BooleanField(
        _("Шаблон курса"),
        default=False,
    )
    is_active = models.BooleanField(
        _("Активен"),
        default=True,
    )
    allow_self_enrollment = models.BooleanField(
        _("Разрешить самостоятельную запись"),
        default=False,
    )
    enrollment_code = models.CharField(
        _("Код записи"),
        max_length=64,
        unique=True,
        blank=True,
        null=True,
    )

    starts_at = models.DateField(
        _("Дата начала курса"),
        blank=True,
        null=True,
    )
    ends_at = models.DateField(
        _("Дата окончания курса"),
        blank=True,
        null=True,
    )
    published_at = models.DateTimeField(
        _("Дата публикации"),
        blank=True,
        null=True,
    )
    archived_at = models.DateTimeField(
        _("Дата архивации"),
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

    objects = CourseManager()

    class Meta:
        db_table = "course_course"
        verbose_name = _("Курс")
        verbose_name_plural = _("Курсы")
        ordering = ("organization", "subject", "-updated_at", "title")
        indexes = [
            models.Index(fields=("status",), name="course_course_status_idx"),
            models.Index(fields=("visibility",), name="course_course_visibility_idx"),
            models.Index(fields=("course_type",), name="course_course_type_idx"),
            models.Index(fields=("owner_teacher",), name="course_course_teacher_idx"),
            models.Index(fields=("organization",), name="course_course_org_idx"),
            models.Index(fields=("subject",), name="course_course_subject_idx"),
            models.Index(fields=("academic_year",), name="course_course_year_idx"),
            models.Index(fields=("period",), name="course_course_period_idx"),
            models.Index(fields=("is_active",), name="course_course_active_idx"),
        ]

    def __str__(self) -> str:
        return self.title

    def clean(self) -> None:
        """
        Проверяет согласованность курса.
        """

        super().clean()

        errors: dict[str, str] = {}

        try:
            validate_course_date_range(
                starts_at=self.starts_at,
                ends_at=self.ends_at,
            )
        except ValidationError as error:
            errors.update(error.message_dict)

        try:
            validate_course_publication_dates(
                published_at=self.published_at,
                archived_at=self.archived_at,
            )
        except ValidationError as error:
            errors.update(error.message_dict)

        if self.course_type == self.CourseTypeChoices.ACADEMIC:
            if not self.organization_id:
                errors["organization"] = _(
                    "Для академического курса нужна организация."
                )

            if not self.subject_id:
                errors["subject"] = _("Для академического курса нужен предмет.")

            if not self.academic_year_id:
                errors["academic_year"] = _(
                    "Для академического курса нужен учебный год."
                )

            if not self.period_id:
                errors["period"] = _("Для академического курса нужен учебный период.")

        if self.period_id and self.academic_year_id:
            if self.period.academic_year_id != self.academic_year_id:
                errors["period"] = _(
                    "Учебный период должен относиться к учебному году курса."
                )

        if self.status == self.StatusChoices.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

        if self.status == self.StatusChoices.ARCHIVED:
            self.is_active = False

            if not self.archived_at:
                self.archived_at = timezone.now()

        if self.visibility == self.VisibilityChoices.PUBLIC_LINK:
            if not self.enrollment_code and self.allow_self_enrollment:
                errors["enrollment_code"] = _(
                    "Для самостоятельной записи по публичной ссылке нужен код записи."
                )

        if errors:
            raise ValidationError(errors)
