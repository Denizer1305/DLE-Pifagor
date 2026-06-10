from __future__ import annotations

from apps.course.constants import (
    COURSE_PLAN_ACADEMIC_YEAR_LABEL_MAX_LENGTH,
    COURSE_PLAN_APPROVED_ORDER_NUMBER_MAX_LENGTH,
    COURSE_PLAN_COMMISSION_NAME_MAX_LENGTH,
    COURSE_PLAN_DISCIPLINE_CODE_MAX_LENGTH,
    COURSE_PLAN_DISCIPLINE_NAME_MAX_LENGTH,
    COURSE_PLAN_ORGANIZATION_NAME_MAX_LENGTH,
    COURSE_PLAN_PROTOCOL_NUMBER_MAX_LENGTH,
    COURSE_PLAN_SPECIALTY_CODE_MAX_LENGTH,
    COURSE_PLAN_SPECIALTY_NAME_MAX_LENGTH,
    COURSE_PLAN_STATUS_APPROVED,
    COURSE_PLAN_STATUS_ARCHIVED,
    COURSE_PLAN_STATUS_DRAFT,
    COURSE_PLAN_STATUS_IMPORTED,
    COURSE_PLAN_STATUS_MAX_LENGTH,
    COURSE_PLAN_STATUS_REVIEWED,
    COURSE_PLAN_TEACHER_NAME_MAX_LENGTH,
    DEFAULT_HOURS,
)
from apps.course.managers import CoursePlanManager
from apps.course.validators import (
    validate_approved_order_data,
    validate_course_plan_hours,
    validate_protocol_data,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class CoursePlan(models.Model):
    """
    Календарно-тематический план курса.

    Шапка КТП вынесена отдельно от Course, чтобы не раздувать
    основную модель курса служебными полями учебно-методического документа.
    """

    class StatusChoices(models.TextChoices):
        DRAFT = COURSE_PLAN_STATUS_DRAFT, _("Черновик")
        IMPORTED = COURSE_PLAN_STATUS_IMPORTED, _("Импортирован")
        REVIEWED = COURSE_PLAN_STATUS_REVIEWED, _("Проверен")
        APPROVED = COURSE_PLAN_STATUS_APPROVED, _("Утверждён")
        ARCHIVED = COURSE_PLAN_STATUS_ARCHIVED, _("Архивирован")

    course = models.OneToOneField(
        "course.Course",
        on_delete=models.CASCADE,
        related_name="plan",
        verbose_name=_("Курс"),
    )

    discipline_name = models.CharField(
        _("Название дисциплины / МДК / практики"),
        max_length=COURSE_PLAN_DISCIPLINE_NAME_MAX_LENGTH,
    )
    discipline_code = models.CharField(
        _("Код дисциплины"),
        max_length=COURSE_PLAN_DISCIPLINE_CODE_MAX_LENGTH,
        blank=True,
    )
    specialty_code = models.CharField(
        _("Код специальности / профессии"),
        max_length=COURSE_PLAN_SPECIALTY_CODE_MAX_LENGTH,
        blank=True,
    )
    specialty_name = models.CharField(
        _("Наименование специальности / профессии"),
        max_length=COURSE_PLAN_SPECIALTY_NAME_MAX_LENGTH,
        blank=True,
    )

    teacher_name_snapshot = models.CharField(
        _("Преподаватель в документе"),
        max_length=COURSE_PLAN_TEACHER_NAME_MAX_LENGTH,
        blank=True,
    )
    organization_name_snapshot = models.CharField(
        _("Организация в документе"),
        max_length=COURSE_PLAN_ORGANIZATION_NAME_MAX_LENGTH,
        blank=True,
    )

    academic_year_label = models.CharField(
        _("Учебный год в документе"),
        max_length=COURSE_PLAN_ACADEMIC_YEAR_LABEL_MAX_LENGTH,
        blank=True,
    )
    semester_number = models.PositiveSmallIntegerField(
        _("Номер семестра"),
        blank=True,
        null=True,
    )

    total_hours = models.PositiveIntegerField(
        _("Всего часов по учебному плану"),
        default=DEFAULT_HOURS,
    )
    semester_hours = models.PositiveIntegerField(
        _("Часов на семестр"),
        default=DEFAULT_HOURS,
    )
    theory_hours = models.PositiveIntegerField(
        _("Теоретические занятия"),
        default=DEFAULT_HOURS,
    )
    practice_hours = models.PositiveIntegerField(
        _("Практические занятия"),
        default=DEFAULT_HOURS,
    )
    lab_hours = models.PositiveIntegerField(
        _("Лабораторные занятия"),
        default=DEFAULT_HOURS,
    )
    self_study_hours = models.PositiveIntegerField(
        _("Самостоятельная работа"),
        default=DEFAULT_HOURS,
    )
    consultation_hours = models.PositiveIntegerField(
        _("Консультации"),
        default=DEFAULT_HOURS,
    )

    commission_name = models.CharField(
        _("Предметная / цикловая комиссия"),
        max_length=COURSE_PLAN_COMMISSION_NAME_MAX_LENGTH,
        blank=True,
    )
    protocol_number = models.CharField(
        _("Номер протокола"),
        max_length=COURSE_PLAN_PROTOCOL_NUMBER_MAX_LENGTH,
        blank=True,
    )
    protocol_date = models.DateField(
        _("Дата протокола"),
        blank=True,
        null=True,
    )
    approved_order_number = models.CharField(
        _("Номер приказа утверждения"),
        max_length=COURSE_PLAN_APPROVED_ORDER_NUMBER_MAX_LENGTH,
        blank=True,
    )
    approved_order_date = models.DateField(
        _("Дата приказа утверждения"),
        blank=True,
        null=True,
    )

    status = models.CharField(
        _("Статус КТП"),
        max_length=COURSE_PLAN_STATUS_MAX_LENGTH,
        choices=StatusChoices.choices,
        default=StatusChoices.DRAFT,
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

    objects = CoursePlanManager()

    class Meta:
        db_table = "course_plan"
        verbose_name = _("КТП курса")
        verbose_name_plural = _("КТП курсов")
        ordering = ("course__organization", "course__subject", "-updated_at")
        indexes = [
            models.Index(fields=("status",), name="course_plan_status_idx"),
            models.Index(fields=("is_active",), name="course_plan_active_idx"),
            models.Index(fields=("semester_number",), name="course_plan_sem_idx"),
        ]

    def __str__(self) -> str:
        return f"КТП: {self.course}"

    def clean(self) -> None:
        """
        Проверяет согласованность КТП.
        """

        super().clean()

        validate_course_plan_hours(
            total_hours=self.total_hours,
            semester_hours=self.semester_hours,
            theory_hours=self.theory_hours,
            practice_hours=self.practice_hours,
            lab_hours=self.lab_hours,
            self_study_hours=self.self_study_hours,
            consultation_hours=self.consultation_hours,
        )
        validate_protocol_data(
            protocol_number=self.protocol_number,
            protocol_date=self.protocol_date,
        )
        validate_approved_order_data(
            approved_order_number=self.approved_order_number,
            approved_order_date=self.approved_order_date,
        )
