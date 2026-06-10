from __future__ import annotations

from apps.course.constants import (
    COURSE_PLAN_IMPORT_FILE_HASH_MAX_LENGTH,
    COURSE_PLAN_IMPORT_FILENAME_MAX_LENGTH,
    COURSE_PLAN_IMPORT_PARSER_VERSION_MAX_LENGTH,
    COURSE_PLAN_IMPORT_STATUS_APPLIED,
    COURSE_PLAN_IMPORT_STATUS_FAILED,
    COURSE_PLAN_IMPORT_STATUS_MAX_LENGTH,
    COURSE_PLAN_IMPORT_STATUS_PARSED,
    COURSE_PLAN_IMPORT_STATUS_UPLOADED,
)
from apps.course.managers import CoursePlanImportManager
from apps.course.validators import validate_course_plan_file_extension
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class CoursePlanImport(models.Model):
    """
    Импорт КТП.

    Модель закладывает будущий парсер DOC/DOCX/PDF, но не требует
    реализации парсинга на текущем этапе.
    """

    class StatusChoices(models.TextChoices):
        UPLOADED = COURSE_PLAN_IMPORT_STATUS_UPLOADED, _("Загружен")
        PARSED = COURSE_PLAN_IMPORT_STATUS_PARSED, _("Разобран")
        FAILED = COURSE_PLAN_IMPORT_STATUS_FAILED, _("Ошибка")
        APPLIED = COURSE_PLAN_IMPORT_STATUS_APPLIED, _("Применён")

    course_plan = models.ForeignKey(
        "course.CoursePlan",
        on_delete=models.CASCADE,
        related_name="imports",
        verbose_name=_("КТП"),
    )
    source_file = models.FileField(
        _("Файл КТП"),
        upload_to="course/ktp/",
        validators=[validate_course_plan_file_extension],
    )
    original_filename = models.CharField(
        _("Исходное имя файла"),
        max_length=COURSE_PLAN_IMPORT_FILENAME_MAX_LENGTH,
        blank=True,
    )
    file_hash = models.CharField(
        _("Хэш файла"),
        max_length=COURSE_PLAN_IMPORT_FILE_HASH_MAX_LENGTH,
        blank=True,
    )

    status = models.CharField(
        _("Статус импорта"),
        max_length=COURSE_PLAN_IMPORT_STATUS_MAX_LENGTH,
        choices=StatusChoices.choices,
        default=StatusChoices.UPLOADED,
    )
    parser_version = models.CharField(
        _("Версия парсера"),
        max_length=COURSE_PLAN_IMPORT_PARSER_VERSION_MAX_LENGTH,
        blank=True,
    )
    parsed_payload = models.JSONField(
        _("Результат разбора"),
        default=dict,
        blank=True,
    )
    errors = models.JSONField(
        _("Ошибки разбора"),
        default=list,
        blank=True,
    )

    imported_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="course_plan_imports",
        verbose_name=_("Кем загружен"),
        blank=True,
        null=True,
    )
    imported_at = models.DateTimeField(
        _("Дата загрузки"),
        default=timezone.now,
    )
    applied_at = models.DateTimeField(
        _("Дата применения"),
        blank=True,
        null=True,
    )

    objects = CoursePlanImportManager()

    class Meta:
        db_table = "course_plan_import"
        verbose_name = _("Импорт КТП")
        verbose_name_plural = _("Импорты КТП")
        ordering = ("-imported_at", "-id")
        indexes = [
            models.Index(fields=("status",), name="course_plan_import_status_idx"),
            models.Index(fields=("course_plan",), name="course_plan_import_plan_idx"),
            models.Index(fields=("imported_by",), name="course_plan_import_user_idx"),
        ]

    def __str__(self) -> str:
        return self.original_filename or f"Импорт КТП #{self.id}"

    def clean(self) -> None:
        """
        Нормализует данные импорта.
        """

        super().clean()

        if self.source_file and not self.original_filename:
            self.original_filename = self.source_file.name
